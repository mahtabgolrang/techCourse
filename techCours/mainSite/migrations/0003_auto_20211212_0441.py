# Generated by Django 3.2.9 on 2021-12-12 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0002_alter_customer_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_pic',
            field=models.ImageField(blank=True, null=True, upload_to='category/coverPictures/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='teacher/profile/picture/'),
        ),
    ]
