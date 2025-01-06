# Generated by Django 5.1.4 on 2025-01-05 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0002_alter_rescisao_contabilidade_rescisao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contratacao',
            name='documentacao_admissional',
        ),
        migrations.AlterField(
            model_name='cadastro',
            name='carteira_trabalho',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='CTPS'),
        ),
        migrations.AlterField(
            model_name='contratacao',
            name='contabilidade_admissional',
            field=models.CharField(blank=True, choices=[('Enviado', 'Enviado'), ('Não Enviado', 'Não Enviado')], max_length=11, null=True, verbose_name='Doc Contabilidade'),
        ),
        migrations.AlterField(
            model_name='contratacao',
            name='status_admissional',
            field=models.BooleanField(default=False, verbose_name='Status Rescisão'),
        ),
        migrations.AlterField(
            model_name='rescisao',
            name='contabilidade_rescisao',
            field=models.CharField(blank=True, choices=[('Enviado', 'Enviado'), ('Não Enviado', 'Não Enviado')], max_length=11, null=True, verbose_name='Contabilidade Documentação'),
        ),
        migrations.AlterField(
            model_name='rescisao',
            name='devolucao_uniforme',
            field=models.CharField(blank=True, choices=[('Entregue', 'Entregue'), ('Não Entregue', 'Não Entregue')], max_length=12, null=True, verbose_name='Devolução Uniforme'),
        ),
    ]
