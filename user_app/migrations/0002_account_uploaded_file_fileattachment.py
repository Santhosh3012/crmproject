# Generated by Django 4.2.5 on 2023-10-04 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10)),
                ('crm_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.account')),
            ],
        ),
    ]