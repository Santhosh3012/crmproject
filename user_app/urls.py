from django.urls import path
from . views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import contacts

urlpatterns = [
    path('register/',register , name='register'),
    path('login/',login , name='login'),
    path('login_success/',login_success, name='login_success'),
    path('forgot_password/',forgot_password, name='forgot_password'),
    path('changepassword/',changepassword, name='changepassword'),
    path('change_password/<int:user_id>/',change_password, name='change_password'),
    # path('dashboard<int:user_id>/', dashboard, name='dashboard'), 
    path('dashboard/', dashboard, name='dashboard'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('profile_view/<int:user_id>/',profile_view,name='profile_view'),
    path('edit_user/<int:user_id>/',edit_user, name='edit_user'),
    path('send_email_two/',send_email_two, name='send_email_two'),
    path('logout/',logout , name='logout'),
    path('create_acc/',create_acc , name='create_acc'),
    path('crm_list/',crm_list , name='crm_list'),
    path('create_crm_contact/',create_crm_contact , name='create_crm_contact'),
    path('crm_contact_list/',crm_contact_list , name='crm_contact_list'),
    path('crm_acc_view/<int:user_id>/',crm_acc_view,name='crm_acc_view'),
    path('delete_crm_acc/<int:user_id>/',delete_crm_acc,name='delete_crm_acc'),
    path('edit_crm_acc/<int:user_id>/',edit_crm_acc, name='edit_crm_acc'),
    # path('file_attachment_list/<int:user_id>/', file_attachment_list, name='file_attachment_list'),
    # path('file_attachments/<int:file_attachment_id>/download/', download_file, name='download_file'),
    path('file_attachments/<int:file_attachment_id>/delete/',delete_file, name='delete_file'),
    path('crm_contact_view/<int:user_id>/',crm_contact_view,name='crm_contact_view'),
    path('edit_crm_contact/<int:user_id>/',edit_crm_contact,name='edit_crm_contact'),
    path('delete_crm_contact/<int:user_id>/',delete_crm_contact,name='delete_crm_contact'),
    path('download_file/<int:company_unique_id>/', download_file, name='download_file'),
    path('delete_file/<int:company_unique_id>/', delete_file, name='delete_file'),
    
    path('contacts/', contacts, name='contacts'),
    
    
    
    # path('add_comment/', views.add_comment, name='add_comment'),
    # path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    # path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





