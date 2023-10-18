from imaplib import _Authenticator
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate , login
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
# from .forms import CustomPasswordChangeForm
import os
from django.shortcuts import get_object_or_404, HttpResponse, redirect
from django.conf import settings




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # Create a new user object
        if password == confirm_password:
            user = User(username=username, email=email, password=password ,)
            
            user.is_registered = True
            user.save()
            
            messages.success(request, f'Hello {user.username}, registration successful. You can now log in.')

            # Redirect to success page
            return render(request,'regsuccess.html', {user:'user'})  # Assuming 'regsuccess' is the URL name for your success page

    return render(request, 'register.html')






def login(request):
    # user=request.user.id
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        user=user.id
        print(">>>>>>>>>>",user)
        if user is not None:
            login(request, user)
           
            user.save()
        #return redirect('login_success',user)
        return HttpResponse(user)
    return render(request, 'login.html')

def login_success(request):

    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        messages.success(request, f'Helloo..{username} Logged in successfully')  # Display success message
        

    return render(request, 'login_success.html')

def forgot_password(request):
    
     return render(request,'forgot_password.html')

def changepassword(request,):

    return render(request, 'changepassword.html')

def logout(request):

    return render(request, 'logout.html')

# def change_password(request,user_id):
#     user = get_object_or_404(User, pk=user_id)
#     if request.method == 'POST':
#         update_password = request.POST['update_password']
#         retypenewpassword = request.POST['retypenewpassword']
#         user=User(update_password=update_password, retypenewpassword=retypenewpassword)
#         user.save()
#         return render(request, 'changepasswordsuccess.html', {'user':user})


def change_password(request, user_id):
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        old_password = User.objects.get(pk=user_id).password
        new_password = request.POST['update_password']
        retyped_password = request.POST['retypenewpassword']
        
        
        if new_password == retyped_password:
                
                user.save()
                # Important: Update the session with the new password
                update_session_auth_hash(request, user)
                return render(request, 'changepasswordsuccess.html', {'user': user})
        else:
                return HttpResponse("New passwords do not match.")
        
    
    return render(request, 'changepassword.html', {'user': user})





def dashboard(request):
    data = User.objects.all().values()
    registered_users = User.objects.filter(is_registered=True)
    context = {'registered_users': registered_users}
    print(registered_users)
    print(">>>>>>",data)
    return render(request, 'dashboard_4_1.html', context)






def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('dashboard')

def profile_view(request,user_id):
   # person = get_object_or_404(Person, pk=person_id)
    user_data = User.objects.get(id=user_id)
    print(type(user_data),user_data)
    # print(type(person),person)
    return render(request, 'profile.html', {'user': user_data})



def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        # Handle form submission and update user data here
        image_file = request.FILES.get('profile')
        user.username = request.POST['username']
        user.email = request.POST['email']
        if image_file:
         user.image = image_file
         user.save()
        
          
        
        return redirect('dashboard')  # Redirect to the dashboard after editing
    
    return render(request, 'edit.html', {'user': user})



def send_email_two(request):
    
    subject = 'Your Old Password Details'  
      # message = "This is your old password " + for_password + " You can use this old password or Enter your new password for your login" # Body of the email
    sender = "confirmationforreg@gmail.com"
    receipent_email = "confirmationforreg@gmail.com"
      
      # send_mail(subject, message, sender, [receipent_email])
      # print("mail sended>>>>>>>")

      #django email function:
      # Load the HTML template file
    template_name = '../templates/send_email.html'
      # template_name = loader.get_template('send_email.html')
    context = {'old_password':"**********"}  # Optional context variables for the template
      # Render the template as a string
    html_message = render_to_string(template_name, context)
      # Convert HTML content to plain text
    plain_message = strip_tags(html_message)
      # subject = 'Your Subject'
      # from_email = 'your-email@example.com'
    to_email = 'recipient-email@example.com'
    email = EmailMessage(subject,  html_message, sender, [receipent_email])
    email.content_subtype = 'html'
      # email.attach_alternative(html_message, "text/html")
    email.send()
    return HttpResponse("Email sent check your inbox")

def create_acc(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        ceo_name = request.POST['ceo_name']
        ceo_email = request.POST['ceo_email']
        country = request.POST['country']
        address = request.POST['address']
        postcode = request.POST['postcode']
        uploaded_file = request.FILES.get('uploaded_file')  # Correct way to get uploaded file
        status = request.POST['status']

        # Create a new account object
        account = Account(
            company_name=company_name,
            ceo_name=ceo_name,
            ceo_email=ceo_email,
            country=country,
            address=address,
            postcode=postcode,
            uploaded_file=uploaded_file,
            status=status
        )
        account.save()

        messages.success(request, f'Account creation successful.')

        # Redirect to success page
        return render(request, 'crm_acc_success.html', {'account': account})

    return render(request, 'crm_account.html')


# def create_acc(request):
#     if request.method == 'POST':
#         company_name = request.POST['company_name']
#         ceo_name = request.POST['ceo_name']
#         ceo_email = request.POST['ceo_email']
#         country = request.POST['country']
#         address = request.POST['address']
#         postcode = request.POST['postcode']
#         uploaded_file = request.FILES.get('uploaded_file')  # Use request.FILES for file uploads
#         status = request.POST['status']

#         account = Account(
#             company_name=company_name,
#             ceo_name=ceo_name,
#             ceo_email=ceo_email,
#             country=country,
#             address=address,
#             postcode=postcode,
#             status=status
#         )
#         account.save()

#         if uploaded_file:
#             file_attachment = FileAttachment(
#                 file_name=uploaded_file.name,
#                 status=status,
#                 crm_account=account
#             )
#             file_attachment.save()

#         messages.success(request, 'Account creation successful.')

#         return render(request, 'crm_acc_success.html', {'account': account})

#     return render(request, 'crm_account.html')



def crm_list(request):
    data = Account.objects.all().values()
   
    
    context = {'data': data}
    
    
    print(">>>>>>",data)
    return render(request, 'crm_acc_list.html', context)




# def create_crm_contact(request):
#     accounts = Account.objects.all()
#     if request.method == 'POST':
#         foreign_key = request.POST.get('foreign_key')
#         company_name = request.POST.get('company_name')
#         display_name = request.POST.get('display_name')
#         decision_maker = request.POST.get('decision_maker')
#         designation = request.POST.get('designation')
#         birthdate = request.POST.get('birthdate')
#         email = request.POST.get('email')
#         department = request.POST.get('department')
#         mobile = request.POST.get('mobile')
#         status = request.POST.get('status')

#         crm_contact = CrmContact(
#             foreign_key=foreign_key,
#             company_name=company_name,
#             display_name=display_name,
#             decision_maker=decision_maker,
#             designation=designation,
#             birthdate=birthdate,
#             email=email,
#             department=department,
#             mobile=mobile,
#             status=status
#         )
#         print(">>>>>>>>>>>",foreign_key,company_name)
#         crm_contact.save()

#         return redirect('crm_contact_list') 
#         # return HttpResponse("success")  # Redirect to a page displaying the list of CRM contacts

#     return render(request, 'crm_contact_page.html',{'accounts': accounts})  # Replace 'your_template.html' with your actual template file


def create_crm_contact(request):
    accounts = Account.objects.all()
    print("########",accounts)

    if request.method == 'POST':
        foreign_key = request.POST.get('foreign_key')
        selected_account = Account.objects.get(company_unique_id=foreign_key)  # Get the associated Account
        display_name = request.POST.get('display_name')
        decision_maker = request.POST.get('decision_maker')
        designation = request.POST.get('designation')
        birthdate = request.POST.get('birthdate')
        email = request.POST.get('email')
        department = request.POST.get('department')
        mobile = request.POST.get('mobile')
        status = request.POST.get('status')

        crm_contact = CrmContact(
            foreign_key=selected_account,  # Assign the Account instance
            company_name=selected_account.company_name,  # Assign the company name from the Account
            display_name=display_name,
            decision_maker=decision_maker,
            designation=designation,
            birthdate=birthdate,
            email=email,
            department=department,
            mobile=mobile,
            status=status
        )
        print(">>>>>>>>>>>",foreign_key,selected_account.company_name)
        crm_contact.save()

        return redirect('crm_contact_list')  # Redirect to a page displaying the list of CRM contacts

    return render(request, 'crm_contact_page.html', {'accounts': accounts})




def crm_contact_list(request):
    crm_contacts = CrmContact.objects.all()
    print("###########",crm_contacts)
    return render(request, 'crm_contact_list.html', {'crm_contacts': crm_contacts})


def crm_acc_view(request,user_id):
   # person = get_object_or_404(Person, pk=person_id)
    acc_data = Account.objects.get(company_unique_id=user_id)
    print(type(acc_data),acc_data)
    # print(type(person),person)
    return render(request, 'view_crm_acc.html', {'acc': acc_data})


def delete_crm_acc(request, user_id):
    crm_acc_data = Account.objects.get(company_unique_id=user_id)
    crm_acc_data.delete()
   
    return redirect('crm_list')

# def edit_crm_acc(request, user_id):
#     acc = get_object_or_404(Account, company_unique_id=user_id)
    
#     if request.method == 'POST':
#         # company_unique_id = request.POST[' company_unique_id']
       
#         acc.company_name = request.POST['company_name']
#         acc.ceo_name = request.POST['ceo_name']
#         acc.ceo_email = request.POST['ceo_email']
#         acc.country = request.POST['country']
#         acc.address = request.POST['address']
#         acc.postcode = request.POST['postcode']
#         acc.uploaded_file = request.POST['uploaded_file']
#         acc.status = request.POST['status']
       
#         acc.save()
#         return redirect('crm_list')
#     return render(request, 'edit_crm_account.html',{'acc':acc})   

from django.core.files.storage import default_storage

def edit_crm_acc(request, user_id):
    acc = get_object_or_404(Account, company_unique_id=user_id)
    
    if request.method == 'POST':
        acc.company_name = request.POST['company_name']
        acc.ceo_name = request.POST['ceo_name']
        acc.ceo_email = request.POST['ceo_email']
        acc.country = request.POST['country']
        acc.address = request.POST['address']
        acc.postcode = request.POST['postcode']
        acc.status = request.POST['status']

        # Handle file upload
        uploaded_file = request.FILES.get('uploaded_file', None)
        if uploaded_file:
            # Save the uploaded file to the media directory
            file_path = default_storage.save(uploaded_file.name, uploaded_file)
            acc.uploaded_file = file_path  # Save the file path to the model

        acc.save()
        return redirect('crm_list')
    
    return render(request, 'edit_crm_account.html', {'acc': acc})

     
        
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Account
# from .forms import YourForm  # Import your form

# def edit_crm_acc(request, user_id):
#     acc = get_object_or_404(Account, company_unique_id=user_id)
    
#     if request.method == 'POST':
#         form = YourForm(request.POST, request.FILES)  # Use your form and pass request.FILES
#         if form.is_valid():
#             # Update the account with the form data
#             acc.company_name = form.cleaned_data['company_name']
#             acc.ceo_name = form.cleaned_data['ceo_name']
#             acc.ceo_email = form.cleaned_data['ceo_email']
#             acc.country = form.cleaned_data['country']
#             acc.address = form.cleaned_data['address']
#             acc.postcode = form.cleaned_data['postcode']
#             acc.uploaded_file = form.cleaned_data['uploaded_file']
#             acc.status = form.cleaned_data['status']
           
#             acc.save()
#             return redirect('crm_list')
#     else:
#         form = YourForm(instance=acc)  # Create a form instance with existing data

#     return render(request, 'edit_crm_account.html', {'acc': acc, 'form': form})

        
# def file_attachment_list(request,user_id):
#     files = Account.objects.get(company_unique_id=user_id)
#     print("$$$",files)
#     return render(request, 'file_attachment_list.html', {'files': files})




def crm_contact_view(request,user_id):
   # person = get_object_or_404(Person, pk=person_id)
    acc_data = CrmContact.objects.get(id=user_id)
    print(type(acc_data),acc_data)
    # print(type(person),person)
    return render(request, 'view_crm_contact.html', {'acc': acc_data})

def edit_crm_contact(request, user_id):
    acc = get_object_or_404(CrmContact, id=user_id)
    
    if request.method == 'POST':
       
      
        acc.display_name = request.POST['display_name']
        acc.decision_maker = request.POST['decision_maker']
        acc.designation = request.POST['designation']
        acc.birthdate = request.POST['birthdate']
        acc.email = request.POST['email']
      
        acc.department=request.POST['department']
        acc.mobile=request.POST['mobile']
        acc.status = request.POST['status']
        # Create a new user object
        acc.save()
        return redirect('crm_contact_list')
    return render(request, 'edit_crm_contact.html',{'acc':acc})    


def delete_crm_contact(request, user_id):
    crm_acc_data =CrmContact.objects.get(id=user_id)
    crm_acc_data.delete()
    return redirect('crm_contact_list')



def download_file(request, company_unique_id):
    account = get_object_or_404(Account, company_unique_id=company_unique_id)

    if account.uploaded_file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(account.uploaded_file))
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_path)
            return response
    else:
        return HttpResponse("File not found")

def delete_file(request, company_unique_id):
    account = get_object_or_404(Account, company_unique_id=company_unique_id)

    if account.uploaded_file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(account.uploaded_file))
        if os.path.exists(file_path):
            os.remove(file_path)
            account.uploaded_file = None  # Clear the uploaded file field
            account.save()
            return redirect('crm_list')  # Redirect to account details page

    return HttpResponse("File not found")
        

def contacts(request):
    data = Account.objects.all().values()
   
    
    context = {'data': data}
    
    
    print(">>>>>>",data)
    return render(request, 'contacts.html', context)


# # views.py

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Comment
# from .forms import CommentForm

# def add_comment(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.save()
#             return redirect('profile')  # Adjust the URL name to your profile view
#     else:
#         form = CommentForm()
#     return render(request, 'add_comment.html', {'form': form})

# def edit_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Adjust the URL name to your profile view
#     else:
#         form = CommentForm(instance=comment)
#     return render(request, 'edit_comment.html', {'form': form})

# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     if request.method == 'POST':
#         comment.delete()
#         return redirect('profile')  # Adjust the URL name to your profile view
#     return render(request, 'delete_comment.html', {'comment': comment})
