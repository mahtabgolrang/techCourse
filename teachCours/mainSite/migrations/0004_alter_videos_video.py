# Generated by Django 3.2.9 on 2021-11-13 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0003_alter_videos_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(upload_to='video/%y'),
        ),
    ]
