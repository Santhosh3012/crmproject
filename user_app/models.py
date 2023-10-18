from django.db import models

# Create your models here.
class User(models.Model):
    image = models.ImageField(upload_to= "pictures/",default= 'pictures/no_image.jpg')
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    

    is_registered = models.BooleanField(default=False) 
    # is_authenticated=models.BooleanField(default=True)

    def __str__(self):
        return self.username
    

class Account(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    company_unique_id = models.AutoField(primary_key=True,null=False) 
    company_name = models.CharField(max_length=255,null=False)
    ceo_name = models.CharField(max_length=255,null=False)
    ceo_email = models.EmailField(max_length=255,null=False) 
    country =  models.CharField(max_length=50,null=False)
    address = models.CharField(max_length=300,null=False)
    postcode = models.CharField(max_length=10,null=False)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Active')
    uploaded_file = models.FileField(upload_to='uploads/', null=True, blank=True)


class CrmContact(models.Model):
    # 1st one choice 2nd one human readable format
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    foreign_key = models.ForeignKey(Account, on_delete=models.CASCADE,null=True) # id from crm account model
    company_name = models.CharField(max_length=255,null=True)                       # company name from crm account model 
    display_name = models.CharField(max_length=255,null=False)  # employee name 
    decision_maker = models.CharField(max_length=10,null=False) # yes or no  
    designation = models.CharField(max_length=255,null=False)   # employee designation  
    birthdate = models.CharField(max_length=100,null=False)     #  employee birth date
    email = models.EmailField(max_length=100,null=False) # employee email
    department = models.CharField(max_length=50,null=False) # employee department
    mobile = models.CharField(max_length=30,null=False) # employee mobile
    created_date = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Active') # employee status


class FileAttachment(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    # Foreign key linking to the Account model
    crm_account = models.ForeignKey('Account', on_delete=models.CASCADE)




    
# # models.py

# from django.db import models
# from django.contrib.auth.models import User

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'Comment by {self.user.username}'
