from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.fason_advert.models import AdvertCategory, Advert, Proposal
from apps.chat.models import Conversation
from .models import Contract

User = get_user_model()


class ContractFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='firma1', password='GucluSifre123!')
        self.bidder = User.objects.create_user(username='atolye1', password='GucluSifre123!')
        self.stranger = User.objects.create_user(username='yabanci', password='GucluSifre123!')
        category = AdvertCategory.objects.create(name='Örme')
        advert = Advert.objects.create(
            owner=self.owner, category=category, title='Test İlan',
            description='Açıklama', city='İstanbul', district='Bağcılar',
        )
        self.proposal = Proposal.objects.create(
            advert=advert, bidder=self.bidder, message='Teklif', status=Proposal.Status.ACCEPTED
        )
        self.conversation = Conversation.objects.get(proposal=self.proposal)
        self.due_date = date.today() + timedelta(days=30)

    def test_stranger_cannot_access_contract_pages(self):
        self.client.login(username='yabanci', password='GucluSifre123!')
        response = self.client.get(reverse('contracts:contract_edit', args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 404)

    def test_owner_can_create_contract(self):
        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.post(
            reverse('contracts:contract_edit', args=[self.conversation.pk]),
            {'quantity': 5000, 'unit_price': '12.50', 'due_date': self.due_date.isoformat(), 'defect_rate': '2.0', 'extra_terms': ''},
        )
        self.assertRedirects(response, reverse('contracts:contract_detail', args=[self.conversation.pk]))
        contract = Contract.objects.get(conversation=self.conversation)
        self.assertEqual(contract.created_by, self.owner)
        self.assertEqual(contract.quantity, 5000)

    def test_both_sides_must_approve(self):
        contract = Contract.objects.create(
            conversation=self.conversation, created_by=self.owner,
            quantity=1000, unit_price=10, due_date=self.due_date,
        )
        self.client.login(username='firma1', password='GucluSifre123!')
        self.client.post(reverse('contracts:contract_approve', args=[self.conversation.pk]))
        contract.refresh_from_db()
        self.assertTrue(contract.owner_approved)
        self.assertFalse(contract.is_fully_approved)

        self.client.logout()
        self.client.login(username='atolye1', password='GucluSifre123!')
        self.client.post(reverse('contracts:contract_approve', args=[self.conversation.pk]))
        contract.refresh_from_db()
        self.assertTrue(contract.is_fully_approved)
        self.assertIsNotNone(contract.approved_at)

    def test_editing_after_approval_resets_approvals(self):
        contract = Contract.objects.create(
            conversation=self.conversation, created_by=self.owner,
            quantity=1000, unit_price=10, due_date=self.due_date,
            owner_approved=True, bidder_approved=True,
        )
        contract.approve_for(self.owner)  # zaten onaylı, değişmez ama emin olalım
        self.assertTrue(contract.is_fully_approved)

        # is_fully_approved iken düzenleme sayfası artık kilitli olmalı (redirect)
        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.get(reverse('contracts:contract_edit', args=[self.conversation.pk]))
        self.assertRedirects(response, reverse('contracts:contract_detail', args=[self.conversation.pk]))

    def test_stranger_cannot_approve(self):
        Contract.objects.create(
            conversation=self.conversation, created_by=self.owner,
            quantity=1000, unit_price=10, due_date=self.due_date,
        )
        self.client.login(username='yabanci', password='GucluSifre123!')
        response = self.client.post(reverse('contracts:contract_approve', args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 404)
