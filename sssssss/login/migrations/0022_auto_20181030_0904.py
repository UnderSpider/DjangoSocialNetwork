# Generated by Django 2.1.2 on 2018-10-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_auto_20181022_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='img',
            name='dianzans',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dianzan',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
