from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('fason_advert', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Teklif Mesajı')),
                ('price_offer', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Teklif Edilen Birim Fiyat (TL)')),
                ('quantity_offer', models.PositiveIntegerField(blank=True, null=True, verbose_name='Karşılanabilecek Adet')),
                ('status', models.CharField(choices=[('PENDING', 'Bekliyor'), ('ACCEPTED', 'Kabul Edildi'), ('REJECTED', 'Reddedildi')], default='PENDING', max_length=10, verbose_name='Durum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Gönderilme Tarihi')),
                ('responded_at', models.DateTimeField(blank=True, null=True, verbose_name='Yanıt Tarihi')),
                ('advert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='fason_advert.advert', verbose_name='İlan')),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to=settings.AUTH_USER_MODEL, verbose_name='Teklif Veren')),
            ],
            options={
                'verbose_name': 'Teklif',
                'verbose_name_plural': 'Teklifler',
                'ordering': ['-created_at'],
                'unique_together': {('advert', 'bidder')},
            },
        ),
    ]