# Generated by Django 5.1.7 on 2025-03-31 00:31

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgis', '0009_entradaestoque_nota_fiscal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entradaestoque',
            name='lote',
        ),
        migrations.RemoveField(
            model_name='entradaestoque',
            name='produto',
        ),
        migrations.RemoveField(
            model_name='entradaestoque',
            name='quantidade',
        ),
        migrations.RemoveField(
            model_name='entradaestoque',
            name='validade',
        ),
        migrations.RemoveField(
            model_name='entradaestoque',
            name='valor_unitario',
        ),
        migrations.AddField(
            model_name='entradaestoque',
            name='data_entrada',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='entradaestoque',
            name='nota_fiscal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgis.notafiscal'),
        ),
        migrations.AlterField(
            model_name='estoque',
            name='ultima_atualizacao',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notafiscal',
            name='numero_nota_fiscal',
            field=models.CharField(default=0, max_length=20, verbose_name='Número da Nota Fiscal'),
        ),
    ]
