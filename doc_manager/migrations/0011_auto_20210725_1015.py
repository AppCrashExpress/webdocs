# Generated by Django 3.2.4 on 2021-07-25 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc_manager', '0010_auto_20210722_1438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id'], 'permissions': [('undelete_order', 'Есть возможность восстанавливать заказы, помеченные на удаление'), ('hard_delete_order', 'Есть возможность удалять заказы, помеченные на удаление')]},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'ordering': ['doc_no'], 'permissions': [('undelete_specification', 'Есть возможность восстанавливать спецификации, помеченные на удаление'), ('hard_delete_specification', 'Есть возможность удалять спецификации, помеченные на удаление')]},
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together={('from_addr', 'to_addr', 'material')},
        ),
    ]
