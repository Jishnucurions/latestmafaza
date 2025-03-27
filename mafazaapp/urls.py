# from django.urls import path
# from .views import CustomLoginView,signup_view,admin_dashboard,user_dashboard,Home

# urlpatterns = [
#     path("",Home,name="home"),
#     # Login
#     path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),

#     # Signup
#     path('signup/', signup_view, name='signup'),

#     # Dashboards
#     path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
#     path('user-dashboard/', user_dashboard, name='user_dashboard'),
# ]

from django.urls import path

from django.contrib.auth.views import LogoutView

from mafazaapp.views import Adminuser, Home, Myproject, admin_dashboard, admin_ledger, admin_view_user_documents,  assign_project, change_password,  create_transaction_view,  custom_login, delete_document, edit_profile, forgot_password,investment_projects, ledger_view, pending_approval, pending_transactions_view,project_list, signup, staff_create_transaction,staff_dashboard, toggle_project_status, update_transaction_status, upload_document, user_logout, view_documents
# from .views import create_transaction,transaction_list,update_transaction_status,pending_approval,AdminLedger,Myproject,create_staff_transaction,toggle_project_status,edit_profile
# from .views import update_return_amount


urlpatterns = [
    path("",Home,name="home"),
    path('signup/', signup, name='signup'),
    path('login/', custom_login, name='login'),
     path('logout/', user_logout, name='logout'),
    path('project_list/',project_list , name='project_list'),
    path("projects/", investment_projects, name="investment_projects"),
     path('assign_project/<uuid:user_id>/', assign_project, name='assign_project'),
    path("staff_dashboard/",staff_dashboard,name="staff_dashboard"),
     path('forgot-password/', forgot_password, name='forgot_password'),
    path('change-password/', change_password, name='change_password'),
    path('documents/delete/<int:doc_id>/', delete_document, name='delete_document'),
    path('pend',pending_transactions_view , name='pend'),
     
     
    
      
    
   
    # path("create_transaction_form/",create_transaction_form,name="create_transaction_form"),
    
      
    path('staff_create_transaction/', staff_create_transaction, name='staff_create_transaction'),
    path('transactions/', create_transaction_view, name='create_transaction'),
    path('ledger/', ledger_view, name='ledger_view'),
     path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path("admin_user/", Adminuser, name="admin_user"),
      path("admin_ledger/", admin_ledger, name="admin_ledger"),
       path('documents/', view_documents, name='view_documents'),
    path('documents/upload/', upload_document, name='upload_document'),

    path('user/<uuid:user_id>/documents/', admin_view_user_documents, name='admin_user_documents'),
        # path('generate-pdf/', generate_ledger_pdf, name='generate_ledger_pdf'),
       
    # path('assign-project/', assign_project, name='assign_project'),
    # path('transactions/new/', create_transaction, name='create_transaction'),
    # path('transactions_list', transaction_list, name='transaction_list'),
    # path('assign-project/<uuid:user_id>/', assign_project, name='assign_project'),
    path('update_transaction/<int:transaction_id>/<str:status>/', update_transaction_status, name='update_transaction_status'),
    path('pending-approval/', pending_approval, name='pending_approval'),
    # path('admin_ledger/', AdminLedger, name='admin_ledger'),
    path('list_project/', Myproject, name='list_project'),
    # path('staff/create-transaction/', create_staff_transaction, name='create_staff_transaction'),
    path('toggle-project-status/<int:project_id>/', toggle_project_status, name='toggle_project_status'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    #  path('update-return-amount/', update_return_amount, name='update_return_amount'),
    
    # path('/', logout, name='logout'),
    
     
   
    
]
   

    

