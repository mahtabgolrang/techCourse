# Generated by Django 3.2.9 on 2021-12-07 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0006_alter_course_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('subject', models.CharField(max_length=30, null=True)),
                ('message', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]