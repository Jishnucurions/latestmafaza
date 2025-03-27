
from datetime import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import DecimalField, ValidationError
from mafazaapp.forms import CustomUserCreationForm, InvestmentProjectForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from .forms import  AssignProjectForm, PasswordEditForm, StaffTransactionForm, UserEditForm
from django.utils.timezone import now
from .forms import TransactionForm
from .utils import create_transaction
from django.shortcuts import render
from django.http import JsonResponse
from .models import AssignedProject
from django.shortcuts import render, get_object_or_404
from .models import AssignedProject, InvestmentProject, CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Transaction, AssignedProject
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Avg,Q
from decimal import Decimal
from django.utils import timezone 
from .forms import PasswordChangeForm
from .models import CustomUser, PasswordResetRequest
import secrets
import string
from django.contrib.auth import authenticate, login
import logging
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required






def Home(request):
    projects = InvestmentProject.objects.filter(is_active=True)  
    return render(request, "home.html", {"projects": projects})






def user_logout(request):
    logout(request)
    response = redirect('login')  # Redirect to login page
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.status = "PENDING"  
            user.save()
            messages.info(request, "Your account is pending approval. You will be notified once approved.")
            return redirect('pending_approval')  
    
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def pending_approval(request):
    return render(request, 'pending_approval.html')




# Set up logging
logger = logging.getLogger(__name__)

# def custom_login(request):
#     debug_info = []  # Store debug information
    
#     if request.method == 'POST':
#         username = request.POST.get('username', '').strip()
#         password = request.POST.get('password', '').strip()
        
#         debug_info.append(f"Login attempt received - Username: '{username}'")
        
#         # Debug: Print raw credentials (remove in production)
#         logger.debug(f"Raw login attempt - Username: {username}, Password: {password}")
        
#         # 1. Check if user exists
#         try:
#             user = CustomUser.objects.get(username=username)
#             debug_info.append(f"User found in database: {user.username} (ID: {user.id})")
#             debug_info.append(f"User active status: {user.is_active}")
#             debug_info.append(f"User status field: {user.status}")
#         except CustomUser.DoesNotExist:
#             messages.error(request, "Username not found")
#             debug_info.append("Username not found in database")
#             logger.warning(f"Failed login attempt - Unknown user: {username}")
#             return render(request, 'login.html', {'debug_info': debug_info})
        
#         # 2. Authenticate
#         auth_user = authenticate(request, username=username, password=password)
#         debug_info.append(f"Authentication result: {auth_user}")
        
#         if auth_user is not None:
#             # 3. Check if user is active
#             if not auth_user.is_active:
#                 messages.error(request, "Account is inactive. Please contact admin.")
#                 debug_info.append("Login failed - Account inactive")
#                 logger.warning(f"Inactive account login attempt: {username}")
#                 return render(request, 'login.html', {'debug_info': debug_info})
            
#             # 4. Login successful
#             login(request, auth_user)
#             debug_info.append("Login successful - session started")
#             logger.info(f"Successful login: {username}")
            
#             # 5. Redirect based on user type
#             if auth_user.is_staff:
#                 debug_info.append("Redirecting to staff dashboard")
#                 return redirect('staff_dashboard')
#             elif auth_user.status == "PENDING":
#                 debug_info.append("Redirecting to pending approval page")
#                 return redirect('pending_approval')
#             else:
#                 debug_info.append("Redirecting to ledger view")
#                 return redirect("ledger_view")
#         else:
#             # Authentication failed
#             debug_info.append("Authentication failed - checking why...")
            
#             # Verify password manually for debugging
#             if user.check_password(password):
#                 debug_info.append("Password verifies with check_password() but authenticate() failed")
#                 debug_info.append("Possible authentication backend issue")
#                 logger.error(f"Authentication backend failure for user {username}")
#             else:
#                 debug_info.append("Password does not match")
#                 logger.warning(f"Invalid password attempt for user {username}")
            
#             messages.error(request, "Invalid username or password")
    
#     # For GET requests or failed POST
#     return render(request, 'login.html', {
#         'debug_info': debug_info,
#         'debug_mode': True  # Set to False in production
#     })

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import logging
from .models import CustomUser

logger = logging.getLogger(__name__)

def custom_login(request):
    debug_info = []  # Store debug information

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        debug_info.append(f"Login attempt received - Username: '{username}'")
        logger.debug(f"Raw login attempt - Username: {username}")

        # 1. Check if user exists
        try:
            user = CustomUser.objects.get(username=username)
            debug_info.append(f"User found in database: {user.username} (ID: {user.id})")
            debug_info.append(f"User active status: {user.is_active}")
            debug_info.append(f"User status field: {user.status}")
        except CustomUser.DoesNotExist:
            messages.error(request, "Username not found")
            debug_info.append("Username not found in database")
            logger.warning(f"Failed login attempt - Unknown user: {username}")
            return render(request, 'login.html', {'debug_info': debug_info})

        # 2. Check password manually instead of authenticate()
        if user.check_password(password):
            debug_info.append("Password is correct")

            # 3. Check if user is active
            if not user.is_active:
                messages.error(request, "Account is inactive. Please contact admin.")
                debug_info.append("Login failed - Account inactive")
                logger.warning(f"Inactive account login attempt: {username}")
                return render(request, 'login.html', {'debug_info': debug_info})

            # 4. Redirect based on status
            if user.status == "PENDING":
                debug_info.append("Redirecting to pending approval page")
                messages.info(request, "Your account is pending approval.")
                return redirect('pending_approval')

            # 5. Log in user manually and redirect
            login(request, user)
            debug_info.append("Login successful - session started")
            logger.info(f"Successful login: {username}")

            # 6. Redirect based on user role
            if user.is_staff:
                debug_info.append("Redirecting to staff dashboard")
                return redirect('staff_dashboard')
            else:
                debug_info.append("Redirecting to ledger view")
                return redirect("ledger_view")
        else:
            debug_info.append("Password does not match")
            messages.error(request, "Invalid username or password")
            logger.warning(f"Invalid password attempt for user {username}")

    return render(request, 'login.html', {
        'debug_info': debug_info,
        'debug_mode': True  # Set to False in production
    })



@login_required(login_url="/login/")
def investment_projects(request):
   
    projects_list = InvestmentProject.objects.all().order_by('-id')  

 
    paginator = Paginator(projects_list, 4)
    page = request.GET.get('page') 

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        
        projects = paginator.page(1)
    except EmptyPage:
      
        projects = paginator.page(paginator.num_pages)

    
    form = InvestmentProjectForm()
    if request.method == "POST":
        form = InvestmentProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("investment_projects")  

    return render(request, "Admin/investment_projects.html", {"projects": projects, "form": form})

def project_list(request):
    projects = InvestmentProject.objects.filter(is_active=True) 
    return render(request, "Admin/project_list.html", {"projects": projects})








# def assign_project(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     projects = InvestmentProject.objects.filter(is_active=True)

#     if request.method == "POST":
#         project_id = request.POST.get("project_id")
#         return_period = request.POST.get("return_period")
#         rate_of_interest = request.POST.get("rate_of_interest")

#         project = get_object_or_404(InvestmentProject, id=project_id)

#         assigned, created = AssignedProject.objects.get_or_create(
#             user=user,
#             project=project,
#             defaults={'return_period': return_period, 'rate_of_interest': rate_of_interest}
#         )

#         if not created:
#             return render(request, "assign_project_form.html", {
#                 "projects": projects,
#                 "user_id": user_id,
#                 "error": "Project already assigned to user!"
#             })

        
#         return redirect("admin_user") 

#     return render(request, "assign_project_form.html", {"projects": projects, "user_id": user_id})


def assign_project(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    projects = InvestmentProject.objects.filter(is_active=True).exclude(
        id__in=user.assigned_projects.values_list('project_id', flat=True)
    )
    assigned_projects = user.assigned_projects.select_related('project').all()

    if request.method == "POST":
        if 'project_id' in request.POST:  # New assignment
            project_id = request.POST.get("project_id")
            return_period = request.POST.get("return_period")
            rate_of_interest = request.POST.get("rate_of_interest")

            project = get_object_or_404(InvestmentProject, id=project_id)

            assigned, created = AssignedProject.objects.get_or_create(
                user=user,
                project=project,
                defaults={
                    'return_period': return_period,
                    'rate_of_interest': rate_of_interest
                }
            )

            if not created:
                return render(request, "assign_project_form.html", {
                    "user": user,
                    "projects": projects,
                    "assigned_projects": assigned_projects,
                    "error": "Project already assigned to user!"
                })

            return redirect("admin_user")

        elif 'edit_id' in request.POST:  # Edit existing assignment
            assigned_id = request.POST.get("edit_id")
            new_roi = request.POST.get("new_roi")
            new_period = request.POST.get("new_period")

            assigned = get_object_or_404(AssignedProject, id=assigned_id, user=user)
            assigned.rate_of_interest = new_roi
            assigned.return_period = new_period
            assigned.save()

            return redirect("admin_user")

    return render(request, "assign_project_form.html", {
        "user": user,
        "projects": projects,
        "assigned_projects": assigned_projects
    })











from django.db.models import Avg, Sum

@staff_member_required
def staff_dashboard(request):
    assigned_projects = AssignedProject.objects.all()

    # Fetch all transactions
    all_transactions = Transaction.objects.select_related('user', 'project').all().order_by('-transaction_date')

    # Calculate required totals from UserLedger
    total_investments = UserLedger.objects.aggregate(Sum('principal_investment'))['principal_investment__sum'] or 0
    total_returns = UserLedger.objects.aggregate(Sum('returns'))['returns__sum'] or 0
    total_withdrawals = UserLedger.objects.aggregate(Sum('withdrawal'))['withdrawal__sum'] or 0
    total_projects = InvestmentProject.objects.count()

    # Calculate total ROI (average rate_of_interest)
    total_roi = AssignedProject.objects.aggregate(Avg('rate_of_interest'))['rate_of_interest__avg'] or 0

    return render(request, "Admin/staff_dashboard.html", {
        "assigned_projects": assigned_projects,
        "all_transactions": all_transactions,
        "total_investments": total_investments,
        "total_returns": total_returns,
        "total_withdrawals": total_withdrawals,
        "total_projects": total_projects,
        "total_roi": total_roi,
    })



# @staff_member_required
# def update_transaction_status(request, transaction_id):
#     transaction = get_object_or_404(Transaction, id=transaction_id)

#     if request.method == "POST":
#         action = request.POST.get("action")
#         if action == "approve":
#             transaction.status = "approved"
#             transaction.save()
#             messages.success(request, f"Transaction {transaction.id} approved.")
#         elif action == "reject":
#             transaction.status = "rejected"
#             transaction.save()
#             messages.success(request, f"Transaction {transaction.id} rejected.")
#         else:
#             messages.error(request, "Invalid action.")

#     return redirect("staff_dashboard")
@staff_member_required
def update_transaction_status(request, transaction_id, status):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if status in ['approved', 'rejected']:
        transaction.status = status
        transaction.save()
        messages.success(request, f"Transaction {transaction.id} {status}.")
    else:
        messages.error(request, "Invalid status.")
    
    return redirect("staff_dashboard")


@login_required(login_url="/login/")
def investment_projects(request):
   
    projects_list = InvestmentProject.objects.all().order_by('-id')  

 
    paginator = Paginator(projects_list, 4)
    page = request.GET.get('page') 

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        
        projects = paginator.page(1)
    except EmptyPage:
      
        projects = paginator.page(paginator.num_pages)

    
    form = InvestmentProjectForm()
    if request.method == "POST":
        form = InvestmentProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("investment_projects") 

    return render(request, "Admin/investment_projects.html", {"projects": projects, "form": form})


def toggle_project_status(request, project_id):
   
    project = get_object_or_404(InvestmentProject, id=project_id)
  
    project.is_active = not project.is_active
    project.save()
    
    
    messages.success(request, f"Project '{project.project_name}' is now {'active' if project.is_active else 'inactive'}.")
    
    
    return redirect('investment_projects')



def Myproject(request):
  
    user = request.user
    
  
    active_projects = InvestmentProject.objects.filter(is_active=True)
    
   
    user_invested_projects = InvestmentProject.objects.filter(
        transactions__user=user  
    ).distinct()

   

    
    return render(request, "User/list_projects.html", {
        "active_projects": active_projects,
        "user_invested_projects": user_invested_projects
    })



from .models import UserLedger







from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserDocument, UserLedger, CustomUser

@login_required
def admin_ledger(request):
    ledger_entries = UserLedger.objects.select_related('transaction__user').all().order_by('date')
    user_type = request.GET.get('user_type', '')
    
    if user_type:
        ledger_entries = ledger_entries.filter(transaction__user__groups__name=user_type)
    
    return render(request, "admin_ledger.html", {
        "ledger_entries": ledger_entries,
        "user_type": user_type
    })

@login_required
def admin_view_user_documents(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    documents = UserDocument.objects.filter(user=user).order_by('-uploaded_at')
    
    return render(request, 'Admin/admin_document_list.html', {
        'user': user,
        'documents': documents
    })





from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TransactionForm
from .models import AssignedProject, Transaction, UserLedger
from .utils import create_transaction
from decimal import Decimal

@login_required(login_url='login')
def create_transaction_view(request):
    projects = AssignedProject.objects.filter(user=request.user)
    current_balance = Decimal('0.00')
    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            try:
                project = form.cleaned_data['project']
                last_ledger = UserLedger.objects.filter(
                    transaction__user=request.user,
                    project_name=project.project_name
                ).order_by('-date').first()
                
                current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
                
                transaction = create_transaction(
                    user=request.user,
                    project=project,
                    amount=form.cleaned_data['amount'],
                    transaction_type=form.cleaned_data['transaction_type'],
                    receipt=form.cleaned_data.get('receipt'),
                    narration=form.cleaned_data['narration']
                )
                
                messages.success(request, 'Transaction created successfully!')
                return redirect('ledger_view')
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = TransactionForm(user=request.user)
        last_ledger = UserLedger.objects.filter(
            transaction__user=request.user
        ).order_by('-date').first()
        current_balance = last_ledger.balance if last_ledger else Decimal('0.00')

    return render(request, 'transactions.html', {
        'form': form,
        'projects': projects,
        'current_balance': current_balance,
        'transactions': transactions
    })

from .utils import generate_missed_returns





# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import TransactionForm
# from .models import AssignedProject, Transaction, UserLedger
# from .utils import create_transaction
# from decimal import Decimal

# def create_transaction_view(request):
#     projects = AssignedProject.objects.filter(user=request.user)
#     current_balance = Decimal('0.00')
#     transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

#     if request.method == 'POST':
#         form = TransactionForm(request.POST, request.FILES, user=request.user)
        
#         if form.is_valid():
#             try:
#                 project = form.cleaned_data['project']
#                 last_ledger = UserLedger.objects.filter(
#                     transaction__user=request.user,
#                     project_name=project.project_name
#                 ).order_by('-date').first()
                
#                 current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
                
#                 transaction = create_transaction(
#                     user=request.user,
#                     project=project,
#                     amount=form.cleaned_data['amount'],
#                     transaction_type=form.cleaned_data['transaction_type'],
#                     receipt=form.cleaned_data.get('receipt'),
#                     narration=form.cleaned_data['narration']
#                 )
                
#                 messages.success(request, 'Transaction created successfully!')
#                 return redirect('ledger_view')
                
#             except Exception as e:
#                 messages.error(request, f'Error: {str(e)}')
#     else:
#         form = TransactionForm(user=request.user)
#         last_ledger = UserLedger.objects.filter(
#             transaction__user=request.user
#         ).order_by('-date').first()
#         current_balance = last_ledger.balance if last_ledger else Decimal('0.00')

#     return render(request, 'transactions.html', {
#         'form': form,
#         'projects': projects,
#         'current_balance': current_balance,
#         'transactions': transactions
#     })

from .utils import generate_missed_returns




@login_required(login_url='login')
def ledger_view(request):
   
    generate_missed_returns()

  
    ledger_entries = UserLedger.objects.filter(
        transaction__user=request.user,
        transaction__status='approved'
    ).order_by('-date')


    projects = AssignedProject.objects.filter(user=request.user)
    
    
    total_investment = UserLedger.objects.filter(
        transaction__user=request.user,
        principal_investment__gt=0
    ).aggregate(total=Sum('principal_investment'))['total'] or Decimal('0.00')

  
    total_balance = Decimal('0.00')
    for project in projects:
        latest_ledger = UserLedger.objects.filter(
            transaction__user=request.user,
            project_name=project.project.project_name
        ).order_by('-date').first()
        if latest_ledger:
            total_balance += latest_ledger.balance

   
    avg_interest_rate = projects.aggregate(
        avg_rate=Avg('rate_of_interest')
    )['avg_rate'] or 0

    
    total_projects = projects.count()

    
    total_withdrawals = UserLedger.objects.filter(
        transaction__user=request.user,
        withdrawal__gt=0
    ).aggregate(total=Sum('withdrawal'))['total'] or Decimal('0.00')

    context = {
        'ledger_entries': ledger_entries,
        'total_investment': total_investment,
        'total_balance': total_balance,
        'avg_interest_rate': avg_interest_rate,
        'total_projects': total_projects,
        'total_withdrawals': total_withdrawals,
    }

    return render(request, 'ledger.html', context)




# def Adminuser(request):
#     users = CustomUser.objects.filter(Q(is_approved=True) | Q(is_staff=True))  
#     pending_users = CustomUser.objects.filter(status='PENDING') 

#     user_type = request.GET.get('user_type', '')
#     search_query = request.GET.get('search', '')

#     if search_query:
#         users = users.filter(username__icontains=search_query)

#     if user_type == "Admin":
#         users = users.filter(is_staff=True)
#     elif user_type == "User":
#         users = users.filter(is_staff=False)

#     # Annotating related fields for investment and returns if applicable
#     # users = users.annotate(
#     #     total_investment=Sum('userledger__principal_investment'),
#     #     total_returns=Sum('userledger__returns')
#     # )

#     if request.method == "POST":
#         user_id = request.POST.get("user_id")
#         action = request.POST.get("action")
#         user = CustomUser.objects.get(id=user_id)

#         if action == "approve":
#             user.status = "APPROVED"
#             user.is_approved = True
#             user.is_active = True
#             if user.is_staff or user.is_superuser:
#                 user.is_approved = True
#                 user.status = "APPROVED"
#             user.save()
#             messages.success(request, f"{user.username} has been approved.")

#         elif action == "reject":
#             user.status = "REJECTED"
#             user.is_approved = False
#             user.is_active = False
#             user.save()
#             messages.error(request, f"{user.username} has been rejected.")

#         elif action == "activate":
#             user.is_active = True
#             user.save()
#             messages.success(request, f"{user.username} has been activated.")

#         elif action == "deactivate":
#             user.is_active = False
#             user.save()
#             messages.warning(request, f"{user.username} has been deactivated.")

#         elif action == "promote":
#             user.is_staff = True
#             user.save()
#             messages.success(request, f"{user.username} has been promoted to Admin.")

#         elif action == "demote":
#             user.is_staff = False
#             user.save()
#             messages.warning(request, f"{user.username} has been demoted to User.")

#         return redirect("admin_user")

#     return render(request, "Admin/admin_user.html", {"users": users, "pending_users": pending_users, "user_type": user_type})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

   
    transactions = Transaction.objects.all().order_by('-date')

   
    total_investments = Transaction.objects.filter(
        transaction_type="investment", status="approved"
    ).aggregate(total=Sum("amount", output_field=DecimalField(max_digits=15, decimal_places=2)))["total"] or 0

   
    total_withdrawals = Transaction.objects.filter(
        transaction_type="withdrawal", status="approved"
    ).aggregate(total=Sum("amount", output_field=DecimalField(max_digits=15, decimal_places=2)))["total"] or 0

    
    

   
    cash_circulation = total_investments - total_withdrawals  

    
    total_projects = InvestmentProject.objects.count()  

    context = {
        'transactions': transactions,
        'total_investments': total_investments,
        'total_withdrawals': total_withdrawals,
        
        'cash_circulation': cash_circulation,
        'total_projects': total_projects
    }

    return render(request, 'Admin/admin_dashboard.html', context)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        
        user_form = UserEditForm(request.POST, instance=request.user)
        password_form = PasswordEditForm(request.user, request.POST)

        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('ledger_view')  

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) 
                messages.success(request, 'Your password was successfully updated!')
                return redirect('ledger_view') 
    else:
        user_form = UserEditForm(instance=request.user)
        password_form = PasswordEditForm(request.user)

    return render(request, 'User/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })

















# @login_required
# def Adminuser(request):
#     if not request.user.is_staff:
#         return redirect('login')
    
#     users = CustomUser.objects.filter(Q(is_approved=True) | Q(is_staff=True))
#     pending_users = CustomUser.objects.filter(status='PENDING')
#     reset_requests = PasswordResetRequest.objects.filter(status='PENDING')
#     temp_password = None  # Initialize variable to store temp password

#     if request.method == "POST":
#         if 'request_id' in request.POST:
#             request_id = request.POST.get("request_id")
#             action = request.POST.get("action")
#             reset_request = PasswordResetRequest.objects.get(id=request_id)
            
#             if action == "approve":
#                 alphabet = string.ascii_letters + string.digits
#                 temp_password = ''.join(secrets.choice(alphabet) for i in range(10))
                
#                 user = reset_request.user
#                 user.set_password(temp_password)
#                 user.save()
                
#                 reset_request.status = "COMPLETED"
#                 reset_request.processed_by = request.user
#                 reset_request.processed_at = timezone.now()
#                 reset_request.temp_password = temp_password
#                 reset_request.save()
                
#                 # Store temp password in session to display
#                 request.session['temp_password'] = temp_password
#                 request.session['temp_username'] = user.username
#                 return redirect('admin_user')  # Redirect to show the password

#             elif action == "reject":
#                 reset_request.status = "REJECTED"
#                 reset_request.processed_by = request.user
#                 reset_request.processed_at = timezone.now()
#                 reset_request.save()
#                 messages.warning(request, "Password reset request rejected")
#                 return redirect('admin_user')

#     # Check if we have a temp password to display
#     if 'temp_password' in request.session:
#         temp_password = request.session.pop('temp_password')
#         username = request.session.pop('temp_username')
#         messages.success(request, f"Temporary password for {username}: {temp_password}")

#     return render(request, "Admin/admin_user.html", {
#         "users": users,
#         "pending_users": pending_users,
#         "reset_requests": reset_requests,
#         "temp_password": temp_password
#     })
@login_required
def Adminuser(request):
    if not request.user.is_staff:
        return redirect('login')
    
    # Get user type filter from GET parameters
    user_type = request.GET.get('user_type', '')
    
    # Base querysets
    users = CustomUser.objects.filter(Q(is_approved=True) | Q(is_staff=True))
    pending_users = CustomUser.objects.filter(status='PENDING')
    reset_requests = PasswordResetRequest.objects.filter(status='PENDING')
    temp_password = None
    
    # Apply user type filter if specified
    if user_type:
        if user_type == 'Admin':
            users = users.filter(is_staff=True)
        elif user_type == 'User':
            users = users.filter(is_staff=False)

    if request.method == "POST":
        # Handle password reset requests
        if 'request_id' in request.POST:
            request_id = request.POST.get("request_id")
            action = request.POST.get("action")
            reset_request = PasswordResetRequest.objects.get(id=request_id)
            
            if action == "approve":
                alphabet = string.ascii_letters + string.digits
                temp_password = ''.join(secrets.choice(alphabet) for i in range(10))
                
                user = reset_request.user
                user.set_password(temp_password)
                user.save()
                
                reset_request.status = "COMPLETED"
                reset_request.processed_by = request.user
                reset_request.processed_at = timezone.now()
                reset_request.temp_password = temp_password
                reset_request.save()
                
                request.session['temp_password'] = temp_password
                request.session['temp_username'] = user.username
                return redirect('admin_user')

            elif action == "reject":
                reset_request.status = "REJECTED"
                reset_request.processed_by = request.user
                reset_request.processed_at = timezone.now()
                reset_request.save()
                messages.warning(request, "Password reset request rejected")
                return redirect('admin_user')

        # Handle user approval/rejection
        elif 'user_id' in request.POST:
            user_id = request.POST.get("user_id")
            action = request.POST.get("action")
            user = CustomUser.objects.get(id=user_id)
            
            if action == "approve":
                user.is_approved = True
                user.status = "APPROVED"
                user.save()
                messages.success(request, f"User {user.username} approved successfully")
                return redirect('admin_user')
                
            elif action == "reject":
                user.is_approved = False
                user.status = "REJECTED"
                user.save()
                messages.warning(request, f"User {user.username} rejected")
                return redirect('admin_user')
                
            elif action in ["activate", "deactivate"]:
                user.is_active = (action == "activate")
                user.save()
                status = "activated" if user.is_active else "deactivated"
                messages.success(request, f"User {user.username} {status} successfully")
                return redirect('admin_user')
                
            elif action in ["promote", "demote"]:
                user.is_staff = (action == "promote")
                user.save()
                role = "admin" if user.is_staff else "regular user"
                messages.success(request, f"User {user.username} is now a {role}")
                return redirect('admin_user')

    # Check if we have a temp password to display
    if 'temp_password' in request.session:
        temp_password = request.session.pop('temp_password')
        username = request.session.pop('temp_username')
        messages.success(request, f"Temporary password for {username}: {temp_password}")

    return render(request, "Admin/admin_user.html", {
        "users": users,
        "pending_users": pending_users,
        "reset_requests": reset_requests,
        "temp_password": temp_password,
        "user_type": user_type
    })
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            PasswordResetRequest.objects.create(user=user)
            messages.info(request, "Password reset request submitted. Contact admin for assistance.")
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, "Username not found")
    
    return render(request, 'forgot_password.html')





@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            
            # Verify current password
            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                # Keep user logged in after password change
                update_session_auth_hash(request, request.user)  
                messages.success(request, "Password changed successfully!")
                return redirect('login')  # Redirect to profile page
    else:
        form = PasswordChangeForm()
    
    return render(request, 'change_password.html', {'form': form})



from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

def is_staff(user):
    return user.is_staff

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect


from django.db.models import Count    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction, AssignedProject, CustomUser
from .forms import StaffTransactionForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StaffTransactionForm
from .models import Transaction, CustomUser, AssignedProject

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

@user_passes_test(lambda u: u.is_staff)
def staff_create_transaction(request):
    if request.method == 'POST':
        form = StaffTransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.status = 'approved'
            
            # Get ROI from the project (using min_roi as default)
            project = form.cleaned_data['project']
            transaction.return_period = 'custom'  # Set appropriate return period
            
            transaction.save()
            
            messages.success(request, 'Transaction created successfully!')
            return redirect('staff_dashboard')
    else:
        form = StaffTransactionForm()
    
    return render(request, 'admin_transactions.html', {'form': form})




# documents/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserDocument
from .forms import DocumentUploadForm

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('view_documents')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'User/upload.html', {'form': form})

# @login_required
# def view_documents(request):
#     documents = UserDocument.objects.filter(user=request.user).order_by('-uploaded_at')
#     return render(request, 'User/list.html', {'documents': documents})

@login_required
def view_documents(request):
    documents = UserDocument.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'User/list.html', {'documents': documents})

@login_required
def delete_document(request, doc_id):
    document = get_object_or_404(UserDocument, id=doc_id, user=request.user)
    
    if request.method == 'POST':
        document.file.delete()  # Delete the actual file
        document.delete()      # Delete the database record
        messages.success(request, 'Document deleted successfully!')
        return redirect('view_documents')
    
    return render(request, 'User/confirm_delete.html', {'document': document})












@staff_member_required
def pending_transactions_view(request):
    # Get all pending transactions (both investment and withdrawal)
    pending_transactions = Transaction.objects.filter(status='pending').order_by('-transaction_date')
    
    return render(request, 'pending_transactions.html', {
        'pending_transactions': pending_transactions
    })
    
    
    