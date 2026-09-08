from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import AdvertCategory, Advert, Proposal

User = get_user_model()


class ProposalFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='firma1', password='GucluSifre123!')
        self.bidder = User.objects.create_user(username='atolye1', password='GucluSifre123!')
        self.category = AdvertCategory.objects.create(name='Örme')
        self.advert = Advert.objects.create(
            owner=self.owner,
            category=self.category,
            title='5000 Adet Örme İş',
            advert_type='job',
            description='Test ilanı',
            city='İstanbul',
            district='Bağcılar',
        )

    def test_owner_cannot_propose_to_own_advert(self):
        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.post(
            reverse('fason_advert:proposal_create', args=[self.advert.slug]),
            {'message': 'Kendi ilanım'},
        )
        self.assertRedirects(response, reverse('fason_advert:detail', args=[self.advert.slug]))
        self.assertEqual(Proposal.objects.count(), 0)

    def test_bidder_can_submit_proposal(self):
        self.client.login(username='atolye1', password='GucluSifre123!')
        response = self.client.post(
            reverse('fason_advert:proposal_create', args=[self.advert.slug]),
            {'message': 'Bu işi alabiliriz', 'price_offer': '12.50', 'quantity_offer': 3000},
        )
        self.assertRedirects(response, reverse('fason_advert:detail', args=[self.advert.slug]))
        self.assertEqual(Proposal.objects.count(), 1)
        proposal = Proposal.objects.first()
        self.assertEqual(proposal.status, Proposal.Status.PENDING)
        self.assertEqual(proposal.bidder, self.bidder)

    def test_cannot_submit_duplicate_pending_proposal(self):
        Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='İlk teklif')
        self.client.login(username='atolye1', password='GucluSifre123!')
        self.client.post(
            reverse('fason_advert:proposal_create', args=[self.advert.slug]),
            {'message': 'İkinci teklif'},
        )
        self.assertEqual(Proposal.objects.filter(advert=self.advert, bidder=self.bidder).count(), 1)

    def test_owner_can_accept_proposal(self):
        proposal = Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='Teklif')
        self.client.login(username='firma1', password='GucluSifre123!')
        self.client.post(reverse('fason_advert:proposal_accept', args=[proposal.pk]))
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, Proposal.Status.ACCEPTED)
        self.assertIsNotNone(proposal.responded_at)

    def test_owner_can_reject_proposal(self):
        proposal = Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='Teklif')
        self.client.login(username='firma1', password='GucluSifre123!')
        self.client.post(reverse('fason_advert:proposal_reject', args=[proposal.pk]))
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, Proposal.Status.REJECTED)

    def test_non_owner_cannot_respond_to_proposal(self):
        proposal = Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='Teklif')
        other_user = User.objects.create_user(username='baskasi', password='GucluSifre123!')
        self.client.login(username='baskasi', password='GucluSifre123!')
        response = self.client.post(reverse('fason_advert:proposal_accept', args=[proposal.pk]))
        self.assertEqual(response.status_code, 404)

    def test_bidder_can_withdraw_pending_proposal(self):
        proposal = Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='Teklif')
        self.client.login(username='atolye1', password='GucluSifre123!')
        self.client.post(reverse('fason_advert:proposal_withdraw', args=[proposal.pk]))
        self.assertEqual(Proposal.objects.count(), 0)

    def test_can_reapply_after_rejection(self):
        proposal = Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='İlk teklif')
        proposal.status = Proposal.Status.REJECTED
        proposal.save()

        self.client.login(username='atolye1', password='GucluSifre123!')
        self.client.post(
            reverse('fason_advert:proposal_create', args=[self.advert.slug]),
            {'message': 'Yeni teklif', 'price_offer': '15.00'},
        )
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, Proposal.Status.PENDING)
        self.assertEqual(proposal.message, 'Yeni teklif')
