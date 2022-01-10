# Generated by Django 2.0 on 2022-01-10 22:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpcionRespuesta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_opcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaPreferencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('textoPregunta', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('option', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='voting.Question')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaBinaria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('respuesta', models.BooleanField(choices=[(1, 'Sí'), (0, 'No')])),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaPreferencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('orden_preferencia', models.PositiveIntegerField(blank=True, null=True)),
                ('opcionRespuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.OpcionRespuesta')),
            ],
        ),
        migrations.CreateModel(
            name='VotacionBinaria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=60)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VotacionPreferencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=60)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
                ('seats', models.PositiveIntegerField(default=1)),
                ('voting_type', models.CharField(choices=[('IDENTITY', 'IDENTITY'), ('WEBSTER', 'WEBSTER'), ('DHONT', 'DHONT'), ('RECUENTO_BORDA', 'RECUENTO_BORDA'), ('RELATIVA', 'RELATIVA'), ('MAYORIA_ABSOLUTA', 'MAYORIA_ABSOLUTA'), ('HAMILTON', 'HAMILTON'), ('SUBTRAC', 'SUBTRAC')], default='IDENTITY', max_length=50)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('tally', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('postproc', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('auths', models.ManyToManyField(related_name='votings', to='base.Auth')),
                ('pub_key', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='voting', to='base.Key')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voting', to='voting.Question')),
            ],
        ),
        migrations.AddField(
            model_name='respuestabinaria',
            name='votacionBinaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.VotacionBinaria'),
        ),
        migrations.AddField(
            model_name='preguntapreferencia',
            name='votacionPreferencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.VotacionPreferencia'),
        ),
        migrations.AddField(
            model_name='opcionrespuesta',
            name='preguntaPreferencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.PreguntaPreferencia'),
        ),
    ]
