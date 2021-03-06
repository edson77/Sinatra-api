# Generated by Django 4.0.4 on 2022-06-01 05:59

import chat.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_user_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_url',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='PNG', keep_meta=True, null=True, quality=75, size=[600, 600], upload_to=chat.models.upload_to),
        ),
    ]
