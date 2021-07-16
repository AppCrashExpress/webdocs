# Generated by Django 3.2.4 on 2021-07-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('doc_manager', '0002_auto_20210716_1344'), ('doc_manager', '0003_auto_20210716_1345')]

    dependencies = [
        ('doc_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specification',
            old_name='number',
            new_name='doc_no',
        ),
        migrations.AlterField(
            model_name='specification',
            name='units',
            field=models.CharField(choices=[('cm3', 'Кубические сантиметры'), ('t', 'Тонны')], max_length=3),
        ),
        migrations.RemoveField(
            model_name='specification',
            name='id',
        ),
        migrations.AlterField(
            model_name='specification',
            name='doc_no',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]