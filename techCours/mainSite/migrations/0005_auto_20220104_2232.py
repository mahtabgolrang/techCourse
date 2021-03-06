# Generated by Django 3.2.9 on 2022-01-04 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0004_teacher_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='course',
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('course', models.ManyToManyField(related_name='transaction', to='mainSite.Course')),
                ('customer', models.ManyToManyField(related_name='transaction', to='mainSite.Customer')),
                ('tacher', models.ManyToManyField(related_name='transaction', to='mainSite.Teacher')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
