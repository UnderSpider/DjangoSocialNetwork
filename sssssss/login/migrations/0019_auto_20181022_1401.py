# Generated by Django 2.1.2 on 2018-10-22 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_auto_20181022_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='usrid',
        ),
        migrations.RenameField(
            model_name='dianzan',
            old_name='user_id',
            new_name='usrid',
        ),
    ]
