# Generated by Django 4.2.7 on 2023-12-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DANI_NAIL_ART', '0004_alter_customuser_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='es_administrador',
            field=models.BooleanField(default=False),
        ),
    ]
