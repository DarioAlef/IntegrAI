# Generated by Django 5.2.1 on 2025-07-14 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_dialoguecontext_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialoguecontext',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dialogue_context', to='core.user'),
        ),
    ]
