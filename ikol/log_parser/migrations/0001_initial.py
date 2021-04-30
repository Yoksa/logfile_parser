# Generated by Django 3.2 on 2021-04-22 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP')),
                ('log_date', models.DateTimeField(auto_now_add=True, verbose_name='Datetime')),
                ('http_method', models.CharField(max_length=12, verbose_name='HTTP method')),
                ('uri_request', models.TextField(verbose_name='URI')),
                ('response_code', models.IntegerField(verbose_name='Code')),
                ('response_len', models.IntegerField(verbose_name='Message length')),
                ('args', models.TextField(verbose_name='Args')),
                ('client', models.TextField(verbose_name='Client info')),
            ],
        ),
    ]
