# Generated by Django 3.2.4 on 2021-08-01 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc_manager', '0019_auto_20210801_1758'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractorexecution',
            options={'ordering': ['date', 'contractor'], 'verbose_name': 'УПД подрядчика', 'verbose_name_plural': 'УПД подрядчика'},
        ),
        migrations.AlterModelOptions(
            name='execution',
            options={'ordering': ['date'], 'verbose_name': 'УПД', 'verbose_name_plural': 'УПД'},
        ),
    ]
