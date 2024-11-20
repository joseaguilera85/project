# clientes/views.py

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import ClienteForm, InteractionForm, SignUpForm, MeetingForm
from .models import Cliente, Interaction, Meeting

### 2.0 Login ###
# Logout the user and redirect to the login page
def logout_view(request):
    logout(request)
    return redirect('menu:login')

#------------------------------------------

# Home page view for authenticated users
@login_required
def client_home(request):
    return render(request, 'clientes/home.html')

#------------------------------------------
def custom_403(request, exception=None): 
    return render(request, 'clientes/403.html', status=403)
#------------------------------------------

### 2.1 Clientes ###

# Create a new client
@login_required
def new_client(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)  # Don't save to the database yet
            cliente.created_by = request.user  # Set the created_by field to the currently logged-in user
            cliente.save()  # Now save the instance to the database
            return redirect('clientes:consult_clients')
    else:
        form = ClienteForm()
        # If the form is not valid, print the error messages
        print("Form is not valid")
    return render(request, 'clientes/new_client.html', {'form': form})


#---------------------------------------------

from django.core.paginator import Paginator

# Consult and filter clients based on search criteria
@login_required
def consult_clients(request):

    # Base query to filter out inactive clients
    #clients = Cliente.objects.exclude(estatus='inactivo')

    search_query = request.GET.get('search', '')
    clients = Cliente.objects.filter(
        Q(nombre__icontains=search_query) |
        Q(apellido__icontains=search_query) |
        Q(mail__icontains=search_query) |
        Q(celular__icontains=search_query)
    ) if search_query else Cliente.objects.all()

    # Paginate the clients
    paginator = Paginator(clients, 20)  # 10 clients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'clientes/client_list.html', {'page_obj': page_obj})


#---------------------------------------------

# Delete a client by ID
@login_required
def delete_client(request, client_id):
    cliente = get_object_or_404(Cliente, id_cliente=client_id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Client deleted successfully!')
        return redirect('clientes:consult_clients')
    return render(request, 'clientes/client_list.html', {'cliente': cliente})

#---------------------------------------------

# Display detailed information about a client, including their interactions
@login_required
def client_detail(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    interactions = client.interactions.all()
    return render(request, 'clientes/client_detail.html', {'client': client, 'interactions': interactions})

#---------------------------------------------

# Edit an existing client's details
@login_required
def edit_client(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client details updated successfully!')
            return redirect('clientes:client_detail', id_cliente=id_cliente)
    else:
        form = ClienteForm(instance=client)
    return render(request, 'clientes/edit_client.html', {'form': form, 'client': client})

#---------------------------------------------

### 2.2 Interacciones ###

# Add an interaction for a specific client
@login_required
def add_interaction(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.cliente = client
            interaction.save()
            messages.success(request, 'Interaction added successfully!')
            return redirect('clientes:client_detail', id_cliente=id_cliente)
    else:
        form = InteractionForm()
    return render(request, 'clientes/add_interaction.html', {'form': form, 'client': client})

#---------------------------------------------
### 2.3 Citas ###

# Schedule a new meeting
from datetime import timedelta
from django.utils.timezone import make_aware

def schedule_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting_date_time = make_aware(meeting.date_time)

            # Check for conflicting meetings
            conflicting_meetings = Meeting.objects.filter(
                salesperson=meeting.salesperson,
                date_time__range=(meeting_date_time - timedelta(minutes=30), meeting_date_time + timedelta(minutes=30))
            )
            if conflicting_meetings.exists():
                messages.error(request, 'This salesperson is already booked at the selected time. Please choose another time.')
                return render(request, 'clientes/schedule_meeting.html', {'form': form})
            
            # Save the meeting
            meeting.save()
            
            # Automatically create an interaction for the meeting
            try:
                Interaction.objects.create(
                    cliente=meeting.client,
                    salesperson=meeting.salesperson,
                    interaction_type='Meeting',
                    category='Follow-up',
                    notes=f"Scheduled a meeting on {meeting.date_time.strftime('%Y-%m-%d %H:%M')}"
                )
            except Exception as e:
                messages.error(request, f"An error occurred while creating the interaction: {str(e)}")
                return render(request, 'clientes/schedule_meeting.html', {'form': form})

            messages.success(request, 'Meeting scheduled successfully!')
            return redirect('clientes:clientes_home')
    else:
        form = MeetingForm()

    return render(request, 'clientes/schedule_meeting.html', {'form': form})


#---------------------------------------------

@login_required
def meeting_list(request):
    # Check for permission
    if not request.user.has_perm('clientes.view_meeting'):
        return render(request, 'clientes/403.html', status=403)
    
    start_date = request.GET.get('start_date', None)
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else timezone.now().date() - timedelta(days=timezone.now().weekday())
    end_of_week = start_date + timedelta(days=6)
    meetings = Meeting.objects.filter(date_time__range=[start_date, end_of_week]).order_by('date_time')
    days = [start_date + timedelta(days=i) for i in range(7)]
    return render(request, 'clientes/meeting_list.html', {'meetings': meetings, 'current_week_start': start_date, 'current_week_end': end_of_week, 'days': days})

#---------------------------------------------


# Edit an existing meeting
@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully!')
            return redirect('clientes:meeting_list')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'clientes/edit_meeting.html', {'form': form, 'meeting': meeting})

#---------------------------------------------

# Delete a meeting by ID
@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted successfully!')
        return redirect('clientes:meeting_list')
    return render(request, 'clientes/delete_meeting.html', {'meeting': meeting})

#---------------------------------------------

def custom_403(request, exception=None): 
    return render(request, 'clientes/403.html', status=403)


#==================

# views.py
# views.py
from django.shortcuts import render
from django.db.models import Count, F, Q  # Add F and Q imports
from .models import Cliente

from django.shortcuts import render
from django.db.models import Count, F, Q
from django.db.models.functions import TruncMonth  # To group by month
from .models import Cliente

from django.db.models import Count, Q, F
from django.db.models.functions import TruncMonth

def dashboard_view(request):
    # Get the total number of leads per month (aggregated by month only)
    new_leads_per_month = Cliente.objects.filter(estatus='lead') \
        .annotate(month=TruncMonth('created_at')) \
        .values('month') \
        .annotate(total_leads=Count('id_cliente')) \
        .order_by('month')

    # Get the total number of leads and clients for each project, with the conversion rate
    project_data = Cliente.objects.values('project') \
        .annotate(total_leads=Count('id_cliente', filter=Q(estatus='lead'))) \
        .annotate(total_clients=Count('id_cliente', filter=Q(estatus='cliente'))) \
        .annotate(conversion_rate=F('total_clients') / F('total_leads') * 100) \
        .order_by('project')

    # Prepare data for the new leads per month chart
    labels = []
    leads_data = []
    for item in new_leads_per_month:
        month_str = item['month'].strftime('%Y-%m')  # Format the month to YYYY-MM
        labels.append(month_str)
        leads_data.append(item['total_leads'])

    # Prepare data for the conversion rate chart
    conversion_labels = []
    conversion_data = []
    for item in project_data:
        conversion_labels.append(item['project'])
        conversion_data.append(item['conversion_rate'])

    # Pass both query results and the chart data to the template
    context = {
        'new_leads_per_month': new_leads_per_month,
        'project_data': project_data,
        'labels': labels,
        'leads_data': leads_data,
        'conversion_labels': conversion_labels,
        'conversion_data': conversion_data,
    }

    return render(request, 'clientes/dashboard.html', context)