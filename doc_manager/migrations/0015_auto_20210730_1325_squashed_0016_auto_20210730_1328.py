# Generated by Django 3.2.4 on 2021-07-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('doc_manager', '0015_auto_20210730_1325'), ('doc_manager', '0016_auto_20210730_1328')]

    dependencies = [
        ('doc_manager', '0014_auto_20210730_1317_squashed_0015_auto_20210730_1317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='execution',
            options={'ordering': ['exec_no']},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'ordering': ['doc_no'], 'permissions': [('undelete_specification', 'Есть возможность восстанавливать спецификации, помеченные на удаление'), ('hard_delete_specification', 'Есть возможность удалять спецификации, помеченные на удаление')]},
        ),
        migrations.AlterField(
            model_name='execution',
            name='exec_no',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='specification',
            name='doc_no',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='execution',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
