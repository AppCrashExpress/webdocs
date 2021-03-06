# Generated by Django 3.2.4 on 2021-07-18 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doc_manager', '0005_auto_20210717_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='doc_manager.driver'),
        ),
        migrations.AddField(
            model_name='order',
            name='real_from_addr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='real_from_addr', to='doc_manager.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='real_to_addr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='real_to_addr', to='doc_manager.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='doc_manager.vehicle'),
        ),
        migrations.AddField(
            model_name='specification',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True),
        ),
        migrations.DeleteModel(
            name='Execution',
        ),
    ]
