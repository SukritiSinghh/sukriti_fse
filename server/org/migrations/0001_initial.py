# Generated by Django 4.2.7 on 2025-02-24 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialInsight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('risk_score', models.FloatField(help_text='Risk score from 0 to 100')),
                ('fraud_alert', models.BooleanField(default=False)),
                ('retention_probability', models.FloatField(help_text='Probability of client retention (0 to 1)')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_insights', to='authentication.organization')),
            ],
            options={
                'verbose_name': 'Financial Insight',
                'verbose_name_plural': 'Financial Insights',
                'unique_together': {('organization', 'year')},
            },
        ),
        migrations.CreateModel(
            name='ChargeSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_expenses', models.DecimalField(decimal_places=2, max_digits=15)),
                ('net_profit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charge_sheets', to='authentication.organization')),
            ],
            options={
                'verbose_name': 'Charge Sheet',
                'verbose_name_plural': 'Charge Sheets',
                'unique_together': {('organization', 'year')},
            },
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('assets', models.DecimalField(decimal_places=2, max_digits=15)),
                ('liabilities', models.DecimalField(decimal_places=2, max_digits=15)),
                ('equity', models.DecimalField(decimal_places=2, max_digits=15)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance_sheets', to='authentication.organization')),
            ],
            options={
                'verbose_name': 'Balance Sheet',
                'verbose_name_plural': 'Balance Sheets',
                'unique_together': {('organization', 'year')},
            },
        ),
    ]
