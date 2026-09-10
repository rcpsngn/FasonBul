from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.fason_advert.models import AdvertCategory, Advert, Proposal
from .models import Conversation, Message

User = get_user_model()


class ConversationAutoCreationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='firma1', password='GucluSifre123!')
        self.bidder = User.objects.create_user(username='atolye1', password='GucluSifre123!')
        category = AdvertCategory.objects.create(name='Örme')
        self.advert = Advert.objects.create(
            owner=self.owner, category=category, title='Test İlan',
            description='Açıklama', city='İstanbul', district='Bağcılar',
        )
        self.proposal = Proposal.objects.create(advert=self.advert, bidder=self.bidder, message='Teklif')

    def test_conversation_created_on_accept(self):
        self.assertFalse(Conversation.objects.filter(proposal=self.proposal).exists())
        self.proposal.status = Proposal.Status.ACCEPTED
        self.proposal.save()
        self.assertTrue(Conversation.objects.filter(proposal=self.proposal).exists())

    def test_no_conversation_on_reject(self):
        self.proposal.status = Proposal.Status.REJECTED
        self.proposal.save()
        self.assertFalse(Conversation.objects.filter(proposal=self.proposal).exists())


class ConversationAccessAndMessagingTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='firma2', password='GucluSifre123!')
        self.bidder = User.objects.create_user(username='atolye2', password='GucluSifre123!')
        self.stranger = User.objects.create_user(username='yabanci', password='GucluSifre123!')
        category = AdvertCategory.objects.create(name='Dokuma')
        self.advert = Advert.objects.create(
            owner=self.owner, category=category, title='Test İlan 2',
            description='Açıklama', city='İstanbul', district='Bağcılar',
        )
        self.proposal = Proposal.objects.create(
            advert=self.advert, bidder=self.bidder, message='Teklif', status=Proposal.Status.ACCEPTED
        )
        self.conversation = Conversation.objects.get(proposal=self.proposal)

    def test_stranger_cannot_view_conversation(self):
        self.client.login(username='yabanci', password='GucluSifre123!')
        response = self.client.get(reverse('chat:conversation_detail', args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 404)

    def test_participants_can_view_conversation(self):
        self.client.login(username='firma2', password='GucluSifre123!')
        response = self.client.get(reverse('chat:conversation_detail', args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 200)

    def test_participant_can_send_message(self):
        self.client.login(username='atolye2', password='GucluSifre123!')
        self.client.post(reverse('chat:conversation_detail', args=[self.conversation.pk]), {'content': 'Merhaba'})
        self.assertEqual(Message.objects.filter(conversation=self.conversation).count(), 1)
        self.assertEqual(Message.objects.first().sender, self.bidder)

    def test_stranger_cannot_send_message(self):
        self.client.login(username='yabanci', password='GucluSifre123!')
        response = self.client.post(reverse('chat:conversation_detail', args=[self.conversation.pk]), {'content': 'Merhaba'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Message.objects.count(), 0)


class MeetingConfirmationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='firma3', password='GucluSifre123!')
        self.bidder = User.objects.create_user(username='atolye3', password='GucluSifre123!')
        category = AdvertCategory.objects.create(name='Kesim')
        self.advert = Advert.objects.create(
            owner=self.owner, category=category, title='Test İlan 3',
            description='Açıklama', city='İstanbul', district='Bağcılar',
        )
        self.proposal = Proposal.objects.create(
            advert=self.advert, bidder=self.bidder, message='Teklif', status=Proposal.Status.ACCEPTED
        )
        self.conversation = Conversation.objects.get(proposal=self.proposal)

    def test_confirmation_requires_both_sides(self):
        self.client.login(username='firma3', password='GucluSifre123!')
        self.client.post(reverse('chat:confirm_meeting', args=[self.conversation.pk]))
        self.conversation.refresh_from_db()
        self.assertTrue(self.conversation.owner_confirmed_meeting)
        self.assertFalse(self.conversation.is_meeting_confirmed)

        self.client.logout()
        self.client.login(username='atolye3', password='GucluSifre123!')
        self.client.post(reverse('chat:confirm_meeting', args=[self.conversation.pk]))
        self.conversation.refresh_from_db()
        self.assertTrue(self.conversation.is_meeting_confirmed)
        self.assertIsNotNone(self.conversation.meeting_confirmed_at)
