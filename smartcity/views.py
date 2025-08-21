from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ServiceProviderR
from .models import CustomerR
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ServiceProviderR
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import ServiceProviderR, CustomerR, ActivityLog, Notification
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator






# Create your views here.


#Service provider Registration page view
def ServiceRegistration(request):
    if request.method=='POST':
        service_image=request.FILES.get('service_image')
        username=request.POST.get('username')
        servicename =request.POST.get('servicename')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        Phoneno=request.POST.get('Phoneno')
        address=request.POST.get('address')
        description=request.POST.get('description')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        #check username already exists or not
        if ServiceProviderR.objects.filter(username=username).exists():
            messages.error(request,'Username already exixts try another')
            return redirect('ServiceProviderRegistration')
        #check if already user registered  using same mail
        if ServiceProviderR.objects.filter(email=email).exists():
            messages.error(request,'User already register by using this email. try new mail to registered')
            return redirect('ServiceProviderRegistration')
        #create service provider instance
        service_provider=ServiceProviderR.objects.create(
            service_image=service_image,
            username=username,
            servicename=servicename,
            first_name=first_name,
            last_name=last_name,
            Phoneno=Phoneno,
            address=address,
            description=description,
            email=email,     
        )
        service_provider.set_password(password)
        service_provider.save()
        messages.success(request,'Serviceprovider is registered successfuly')
        return redirect('/ServiceProviderRegistration/')
            
        
    return render(request,'ServiceproviderReg.html')



# customer registration page view
def CustomerReg(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if CustomerR.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('CustomerReg')
        customer=CustomerR.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )
        customer.set_password(password)
        customer.save()
        messages.success(request,'Customer Registered successfuly')
        return redirect('CustomerReg')
        
        
    return render(request,'CustomerRegistration.html')

#home page view
def Home(request):
    return render(request,'Home.html')


#about page view
def About(request):
    return render(request,'about.html')


#login view page
def Loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')
        
        # Check Service Provider
        try:
            provider = ServiceProviderR.objects.get(username=username)
            if check_password(password, provider.password):
                request.session['user_type'] = 'provider'
                request.session['user_id'] = provider.id
                request.session['is_logged_in'] = True
                messages.success(request, 'Login successful')
                
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                ):
                    return redirect(next_url)
                return redirect('Home')
        except ServiceProviderR.DoesNotExist:
            pass
        
        # Check Customer
        try:
            customer = CustomerR.objects.get(username=username)
            if check_password(password, customer.password):
                request.session['user_type'] = 'customer'
                request.session['user_id'] = customer.id
                request.session['is_logged_in'] = True
                messages.success(request, 'Login successful')
                
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                ):
                    return redirect(next_url)
                return redirect('Home')
        except CustomerR.DoesNotExist:
            pass
        
        messages.error(request, "Invalid username or password.")
        return redirect(f'Loginpage?next={next_url}' if next_url else 'Loginpage')
    
    next_url = request.GET.get('next', '')
    return render(request, 'Login.html', {'next_url': next_url})


#plumber view
def Plumber(request):
    # Authentication check
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Plumber/')
    
    # Base queryset without select_related
    queryset = ServiceProviderR.objects.filter(
        servicename__iexact='plumber',
        
    ).order_by('-rating')  # Removed select_related
    
    # Location filtering
    location = request.GET.get('location', '').strip()
    if location:
        queryset = queryset.filter(address__icontains=location)
        page_title = f"Plumbers in {location}"
    else:
        page_title = "Professional Plumbers"
    
    # Prepare context
    context = {
        'plumbers': queryset,
        'page_title': page_title,
        'search_location': location,
        'user_type': request.session.get('user_type'),
        'user_id': request.session.get('user_id')  # Added for template checks
    }
    
    return render(request, 'Plumber.html', context)


#Electrician view page
def Electricion(request):
    #authentication check
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Electricion/')
    
    # Base queryset without select_related
    queryset=ServiceProviderR.objects.filter(
    servicename__iexact='electrician'  # 
).order_by('-rating')
    
    #locations filtring
    location=request.GET.get('location','').strip()
    if location:
        queryset=queryset.filter(address__icontains=location)
        page_title=f"Electrician in {location}"
    else:
        page_title='Porfessional Electrician'
        
    #context
    context={
        'electricians':queryset,
        'page_title': page_title,
        'search_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id')
        
    }
    return render(request,'Electricion.html',context)
#carpenters view page   
def Carpenter(request):
    #authentication check
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Carpenter/')
    
    #base querywothout select related
    queryset=ServiceProviderR.objects.filter(
        servicename__iexact='carpenter'
    ).order_by('-rating')
    #location
    location=request.GET.get('location','')
    if location:
        queryset=queryset.filter(address__icontains=location)
        page_title=f"Carpenter in {location}"
    else:
        page_title="Professional Carpenters"
    context={
        'carpenters':queryset,
        'page_title':page_title,
        'search_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id') 
    }
    return render(request,'Carpenter.html',context)

#painter view page
def Painter(request):
    #authenticate check
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Painter/')
    
    #base query without select
    queryset=ServiceProviderR.objects.filter(
        servicename__iexact='painter'
    ).order_by('-rating')
    
    #search section
    location=request.GET.get('location','')
    if location:
        queryset=queryset.filter(address__icontains='painter')
        page_title=f'Painter in {location}'
    else:
        page_title='Professional Painters'
    
    context={
        'painters':queryset,
        'page_title':page_title,
        'search_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id')
    }
    
    return render(request,'Painter.html',context)

def Welder(request):
    #authenticate
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Welder/')
    
    #base query without searching
    queryset=ServiceProviderR.objects.filter(
        servicename__iexact='welder'
    ).order_by('-rating')
    
    #location searching
    location=request.GET.get('location','')
    if location:
        queryset=queryset.filter(address__icontains=location)
        page_title=f'Welders in {location}'
    else:
        page_title='Professional welders'
        
    context={
        'welders':queryset,
        'page_title':page_title,
        'search_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id')
    }
    return render(request,'Welder.html',context)
    
#cable provider
def CableProvider(request):
    #authenticate
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/CableProvider/')
    
    #base query select
    queryset=ServiceProviderR.objects.filter(
        servicename__iexact='cable'
        ).order_by('-rating')
    location=request.GET.get('location','')
    if location:
        queryset=queryset.filter(address__icontains=location)
        page_title=f'Cable Providers in {location}'
    else:
        page_title='Professional Cable Providers'
    
    context={
        'cableproviders':queryset,
        'page_title':page_title,
        'search_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id')
    }
   
    return render(request,'CableProvider.html',context)
#Internet view logic
def Internat(request):
    #authenticate
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Internet/')
    
    #base query
    queryset=ServiceProviderR.objects.filter(
        servicename__iexact='internet'
    ).order_by('-rating')
    
    
    #location search
    location=request.session.get('location','')
    if location:
        queryset=queryset.filter(address__icontains=location)
        page_title=f'Internat provider in {location}'
    else:
        page_title='Professionals Internat Providers'
        
    context={
        'internats':queryset,
        'page_title':page_title,
        'search_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id')
    }
    return render(request,'Internet.html',context)
#groceries view
#groceries provider
def Groceries(request):
    if not request.session.get('is_logged_in'):
        return redirect('/Loginpage/?next=/Groceries/')
    
    #base query
    queryset=ServiceProviderR.objects.filter(
        servicename__iexact='groceries'
    ).order_by('-rating')
    
    location=request.GET.get('location','')
    if location:
        queryset=queryset.filter(address__icontains=location)
        page_title=f'Groceries Provider {location}'
    else:
        page_title='Professional Groceries Provider'
        
    context={
        'groceries':queryset,
        'page_title':page_title,
        'seacrh_location':location,
        'user_type':request.session.get('user_type'),
        'user_id':request.session.get('user_id')
    }
    
    return render(request,'Groceries.html',context)
#logout view
def logout_view(request):
    # Clear session data
    request.session.flush()
    # Redirect to home page after logout
    return redirect('/Home/')


#admin login page
@require_http_methods(["GET", "POST"])
def admin_login(request):
    # Redirect if already logged in as superuser
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/dashboard/')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate inputs
        if not username or not password:
            messages.error(request, 'Both fields are required')
            return render(request, 'admin_login.html')
        
        # Authenticate using Django's built-in auth
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                # Create activity log
                ActivityLog.objects.create(
                    activity_type='login',
                    message=f'Admin {user.username} logged in',
                    user=user  # Assuming your ActivityLog has a user field
                )
                return redirect('dashboard')
            else:
                messages.error(request, 'Admin privileges required')
        else:
            messages.error(request, 'Invalid credentials')
        
        return render(request, 'admin_login.html')
    
    return render(request, 'admin_login.html')





#admin dashboard view
def dashboard(request):
    # Redirect non-admin users
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('admin:login')
    
    # Calculate date ranges for statistics
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    
    # User statistics (only staff users)
    total_users = CustomerR.objects.count()
    last_month_users = CustomerR.objects.filter().count()
    user_growth = calculate_growth(total_users, last_month_users)
    
    # Service Provider statistics
    total_providers = ServiceProviderR.objects.count()
    
    
    # Approval statistics
    approval_counts = {
        'approved': ServiceProviderR.objects.filter(is_approved=True).count(),
        'pending': ServiceProviderR.objects.filter(is_approved=False).count(),
       
    }
    
    # New approvals in the last week
    new_approvals = ServiceProviderR.objects.filter(
        is_approved=True, 
        
    ).count()
    
    # Pending reviews
    pending_reviews = approval_counts['pending']
    
    # Service type distribution
    service_counts = {
        'plumber': ServiceProviderR.objects.filter(servicename='plumber').count(),
        'electrician': ServiceProviderR.objects.filter(servicename='electrician').count(),
        'carpenter': ServiceProviderR.objects.filter(servicename='carpenter').count(),
        'painter': ServiceProviderR.objects.filter(servicename='painter').count(),
        'welder': ServiceProviderR.objects.filter(servicename='welder').count(),
        'Cable': ServiceProviderR.objects.filter(servicename='cable').count(),
        'internet': ServiceProviderR.objects.filter(servicename='internet').count(),
        'groceries': ServiceProviderR.objects.filter(servicename='groceries').count(),
    }
    
    # Recent activities (last 10)
    recent_activities = ActivityLog.objects.all().order_by('-timestamp')[:10]
    
    # Recent service providers (last 5)
    recent_providers = ServiceProviderR.objects.order_by('-id')[:5]
    
    # Unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user, 
        is_read=False
    ).order_by('-created_at')
    
    context = {
        'total_users': total_users,
        'user_growth': user_growth,
        'total_providers': total_providers,
        'approval_counts': approval_counts,
        'new_approvals': new_approvals,
        'pending_reviews': pending_reviews,
        'service_counts': service_counts,
        'recent_activities': recent_activities,
        'recent_providers': recent_providers,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'Dashboard.html', context) 
#calculate the providers
def calculate_growth(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 1)
def calculate_growth(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 1)
    



#provider approved 
@require_POST
@csrf_exempt
@login_required
def approve_provider(request, provider_id):
    try:
        provider = ServiceProviderR.objects.get(id=provider_id)
        provider.is_approved = True
        provider.is_rejected = False
        provider.save()
        
        return JsonResponse({
            'success': True,
            'new_status': 'approved',
            'status_badge': '''
                <span class="badge badge-success">
                    <i class="fas fa-check-circle"></i> Approved
                </span>
            ''',
            'provider_id': provider_id
        })
    except ServiceProviderR.DoesNotExist:
        return JsonResponse(
            {'success': False, 'message': 'Provider not found'}, 
            status=404
        )


#provider reject
@require_POST
@csrf_exempt
@login_required
def reject_provider(request, provider_id):
    try:
        provider = ServiceProviderR.objects.get(id=provider_id)
        provider.is_approved = False
        provider.is_rejected = True
        provider.save()
        
        return JsonResponse({
            'success': True,
            'new_status': 'rejected',
            'status_badge': '''
                <span class="badge badge-danger">
                    <i class="fas fa-times-circle"></i> Rejected
                </span>
            ''',
            'provider_id': provider_id
        })
    except ServiceProviderR.DoesNotExist:
        return JsonResponse(
            {'success': False, 'message': 'Provider not found'}, 
            status=404
        )





#service provider admin page
def service_providers(request):
    providers = ServiceProviderR.objects.all().order_by('approval_date')
    
    # Filtering
    service_type = request.GET.get('service')
    if service_type:
        providers = providers.filter(servicename=service_type)
    
    approval_status = request.GET.get('status')
    if approval_status == 'approved':
        providers = providers.filter(is_approved=True)
    elif approval_status == 'pending':
        providers = providers.filter(is_approved=False)
    
    search_query = request.GET.get('search')
    if search_query:
        providers = providers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(Phoneno__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(providers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'providers': page_obj,
        'service_type': service_type,
        'approval_status': approval_status,
        'search_query': search_query,
    }
    return render(request, 'service_providers.html', context)



#admin servcie rpoviders editing page
def edit_provider(request, provider_id):
    provider = get_object_or_404(ServiceProviderR, id=provider_id)
    service_choices = ServiceProviderR.SERVICE_CHOICES
    
    if request.method == 'POST':
        try:
            # Update provider details
            provider.username = request.POST.get('username')
            provider.first_name = request.POST.get('first_name')
            provider.last_name = request.POST.get('last_name')
            provider.email = request.POST.get('email')
            provider.Phoneno = request.POST.get('Phoneno')
            provider.address = request.POST.get('address')
            provider.servicename = request.POST.get('servicename')
            provider.description = request.POST.get('description', '')
            
            # Handle approval status
            is_approved = request.POST.get('is_approved') == 'true'
            if is_approved and not provider.is_approved:
                provider.approval_date = timezone.now()
            provider.is_approved = is_approved
            
            # Handle rating
            try:
                provider.rating = float(request.POST.get('rating', 0))
            except (ValueError, TypeError):
                provider.rating = 0.0
            
            # Handle service image
            if 'service_image' in request.FILES:
                provider.service_image = request.FILES['service_image']
            
            provider.save()
            
            messages.success(request, 'Service provider updated successfully!')
            return redirect('service_providers')
            
        except Exception as e:
            messages.error(request, f'Error updating provider: {str(e)}')
            # For AJAX responses
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
    
    context = {
        'provider': provider,
        'service_choices': service_choices
    }
    
    return render(request, 'edit_provider.html', context)

#admin service provider viewss page

@login_required
def service_provider_view(request, provider_id):
    provider = get_object_or_404(ServiceProviderR, id=provider_id)
    
    # Determine if the provider is verified (you can adjust this logic as needed)
    is_verified = provider.is_approved  # Or any other verification logic you have
    
    context = {
        'provider': provider,
        'date_joined': provider.approval_date.strftime("%B %d, %Y") if provider.approval_date else "Not approved yet",
        'servicename': provider.get_servicename_display(),  # This will show the display name of the choice
        'page_title': f'{provider.first_name} {provider.last_name} | Details',
        'is_verified': is_verified,
    }
    
    return render(request, 'serviceprovider_view.html', context)


#admin customer view
def customers(request):
    # Get all customers from CustomerR model
    customers = CustomerR.objects.all().order_by('-id')
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter == 'verified':
        customers = customers.filter(is_active=True)
    elif status_filter == 'unverified':
        customers = customers.filter(is_active=False)
    
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query))
    
    # Pagination
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
    }
    return render(request, 'Customer_admin.html', context)

#admin customer view page
@login_required
def customer_detail(request, customer_id):
    # Get the customer or return 404
    customer = get_object_or_404(CustomerR, id=customer_id)
    
    # Get recent activities (you can customize this based on your needs)
    activities = [
        {
            'icon': 'user',
            'title': 'Account created',
            'date': customer.date_joined if hasattr(customer, 'date_joined') else "Unknown"
        },
        # Add more activities as needed
    ]
    
    context = {
        'customer': customer,
        'activities': activities,
    }
    
    return render(request, 'customer_detail.html', context)


















#chatbot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import re
import random
from django.urls import reverse
from .models import ServiceProviderR  # Your model

@csrf_exempt
def jarvis_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').lower().strip()
            
            # First check for greetings
            greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
            if any(greet in query for greet in greetings):
                responses = [
                    "Hello! I'm your SmartCityConnect assistant. How can I help you today?",
                    "Hi there! I'm your SmartCityConnect assistant, What service are you looking for today?",
                    "Greetings! I'm your SmartCityConnect assistant, I can help you find local service providers. What do you need?",
                    "Hello! I'm your SmartCityConnect assistant, I can connect you with plumbers, electricians, painters and more. What service do you require?"
                ]
                return JsonResponse({
                    'status': 'success',
                    'response': random.choice(responses)
                })
            
            # Check for thanks/bye
            farewells = ['thanks','thankyou' ,'thank you','by', 'bye', 'goodbye', 'see you', 'good night']
            if any(word in query for word in farewells):
                responses = [
                    "You're welcome! Let me know if you need anything else.",
                    "Happy to help! Come back anytime you need service providers.",
                    "Goodbye! Remember SmartCityConnect is here when you need services.",
                    "Thank you for using SmartCityConnect! Have a great day!",
                    "See you later! Don't hesitate to ask if you need more help.",
                    "Goodbye! We're always here to connect you with great service providers."
                ]
                return JsonResponse({
                    'status': 'success',
                    'response': random.choice(responses),
                    'providers': []
                })

            # Normalize service name spellings
            def normalize_service_name(name):
                name = name.lower().strip()
                corrections = {
                    'electrition': 'electrician',
                    'electrian': 'electrician',
                    'weldr': 'welder',
                    'paintor': 'painter',
                    'plumb': 'plumber',
                    'carpent': 'carpenter',
                    'internet': 'internet',
                    'groceries': 'groceries',
                    'cable': 'cable'
                }
                return corrections.get(name, name)

            # Normalize query text
            def normalize_query(text):
                text = re.sub(r'[^a-z0-9 ]', '', text)
                corrections = {
                    'electri': 'electric',
                    'weldr': 'weld',
                    'paintor': 'paint',
                    'plumb': 'plumb',
                    'cabl': 'cable'
                }
                for wrong, right in corrections.items():
                    text = text.replace(wrong, right)
                return text

            normalized_query = normalize_query(query)

            # Get all available services (normalized)
            raw_services = ServiceProviderR.objects.filter(
                is_approved=True
            ).values_list('servicename', flat=True).distinct()

            available_services = {normalize_service_name(s) for s in raw_services}

            # Master keyword mapping (using normalized service names)
            SERVICE_KEYWORDS = {
                # Plumbing
                'plumb': 'plumber',
                'leak': 'plumber',
                'pipe': 'plumber',
                'water': 'plumber',
                # Electrical
                'electric': 'electrician',
                'power': 'electrician',
                'wiring': 'electrician',
                'light': 'electrician',
                # Carpentry
                'carpent': 'carpenter',
                'wood': 'carpenter',
                'furniture': 'carpenter',
                'door': 'carpenter',
                # Painting
                'paint': 'painter',
                'wall': 'painter',
                'color': 'painter',
                # Welding
                'weld': 'welder',
                'metal': 'welder',
                'iron': 'welder',
                # Cable
                'cable': 'cable',
                'tv': 'cable',
                'television': 'cable',
                # Internet
                'internet': 'internet',
                'wifi': 'internet',
                # Groceries
                'grocery': 'groceries',
                'food': 'groceries'
            }

            # Find matching service
            matched_service = None
            for keyword, service in SERVICE_KEYWORDS.items():
                if keyword in normalized_query and service in available_services:
                    matched_service = service
                    break

            if matched_service:
                # Map service names to your URL patterns
                service_url_map = {
                    'electrician': 'Electricion',
                    'carpenter': 'Carpenter',
                    'painter': 'Painter',
                    'welder': 'Welder',
                    'cable': 'CableProvider',
                    'internet': 'Internat',
                    'groceries': 'Groceries',
                    'plumber': 'Plumber'  # Add this if you have a Plumber URL
                }
                
                # Get the URL name or default to service name if not found
                url_name = service_url_map.get(matched_service)
                if url_name:
                    try:
                        service_url = reverse(url_name)
                    except:
                        service_url = f'/{matched_service}/'
                else:
                    service_url = f'/{matched_service}/'

                # Find providers with exact service name match
                providers = ServiceProviderR.objects.filter(
                    Q(servicename=matched_service) & 
                    Q(is_approved=True)
                ).order_by('-rating')[:5]

                providers_data = []
                for p in providers:
                    providers_data.append({
                        'name': f"{p.first_name} {p.last_name}",
                        'phone': p.Phoneno,
                        'rating': float(p.rating),
                        'address': p.address,
                        'description': p.description or "No description provided",
                        'image': p.service_image.url if p.service_image else None
                    })

                if providers_data:
                    return JsonResponse({
                        'status': 'success',
                        'service': matched_service,
                        'providers': providers_data,
                        'response': (
                            f"I found {len(providers_data)} {matched_service} providers. " +
                            f"<a href='{service_url}' class='service-link'>View all {matched_service} providers</a> " 
                        )
                    })
                else:
                    return JsonResponse({
                        'status': 'no_providers',
                        'response': (
                            f"No {matched_service} providers available right now. " +
                            f"<a href='{service_url}' class='service-link'>Check {matched_service} page</a> " +
                            f"or <a href='/' class='service-link'>try another service</a>"
                        )
                    })
            else:
                # Build suggestions based on available services
                service_keywords = {
                    'plumber': ['leak', 'pipe', 'water'],
                    'electrician': ['power', 'wiring', 'lights'],
                    'carpenter': ['furniture', 'wood', 'doors'],
                    'painter': ['wall', 'paint', 'color'],
                    'welder': ['metal', 'weld', 'iron'],
                    'cable': ['TV', 'cable', 'television'],
                    'internet': ['wifi', 'internet', 'router'],
                    'groceries': ['food', 'grocery', 'vegetables']
                }

                suggestions = []
                for service in available_services:
                    if service in service_keywords:
                        examples = service_keywords[service][:3]
                        url_name = service_url_map.get(service, service)
                        try:
                            service_url = reverse(url_name)
                        except:
                            service_url = f'/{service}/'
                            
                        suggestions.append(
                            f"<a href='{service_url}' class='service-link'>{service}</a> " +
                            f"(e.g. {', '.join(examples)})"
                        )

                return JsonResponse({
                    'status': 'unknown',
                    'response': (
                        "I can help with:<br>• " + "<br>• ".join(suggestions) + 
                        "<br><br><a href='/' class='service-link'>Browse all services</a>"
                    )
                })

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'response': "I'm having trouble. Please try again later."
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'response': 'Invalid request method'}, 
        status=400)