# Generated by Django 2.0 on 2022-01-12 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='voting_type',
            field=models.CharField(choices=[('IDENTITY', 'IDENTITY'), ('WEBSTER', 'WEBSTER'), ('DHONT', 'DHONT'), ('RECUENTO_BORDA', 'RECUENTO_BORDA'), ('RELATIVA', 'RELATIVA'), ('MAYORIA_ABSOLUTA', 'MAYORIA_ABSOLUTA'), ('HAMILTON', 'HAMILTON'), ('WEBSTER_MODIFICADO', 'WEBSTER_MODIFICADO'), ('SUBTRAC', 'SUBTRAC')], default='IDENTITY', max_length=50),
        ),
    ]
