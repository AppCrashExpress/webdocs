# Generated by Django 3.2.4 on 2021-07-16 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc_manager', '0002_auto_20210716_1344_squashed_0003_auto_20210716_1345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='execution',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['specification']},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'ordering': ['doc_no']},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['car_id']},
        ),
    ]