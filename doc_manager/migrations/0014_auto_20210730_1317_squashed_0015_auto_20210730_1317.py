# Generated by Django 3.2.4 on 2021-07-30 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('doc_manager', '0014_auto_20210730_1317'), ('doc_manager', '0015_auto_20210730_1317')]

    dependencies = [
        ('doc_manager', '0013_auto_20210729_1530'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='execution',
            options={},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'permissions': [('undelete_specification', 'Есть возможность восстанавливать спецификации, помеченные на удаление'), ('hard_delete_specification', 'Есть возможность удалять спецификации, помеченные на удаление')]},
        ),
        migrations.RenameField(
            model_name='execution',
            old_name='exec_no',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='specification',
            old_name='doc_no',
            new_name='id',
        ),
        migrations.AddField(
            model_name='execution',
            name='exec_no',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='doc_no',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
    ]
