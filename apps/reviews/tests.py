from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.fason_advert.models import AdvertCategory, Advert, Proposal
from apps.chat.models import Conversation
from apps.contracts.models import Contract
from .models import Review

User = get_user_model()


class ReviewFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='firma1', password='GucluSifre123!')
        self.bidder = User.objects.create_user(username='atolye1', password='GucluSifre123!')
        self.stranger = User.objects.create_user(username='yabanci', password='GucluSifre123!')
        category = AdvertCategory.objects.create(name='Örme')
        advert = Advert.objects.create(
            owner=self.owner, category=category, title='Test İlan',
            description='Açıklama', city='İstanbul', district='Bağcılar',
        )
        proposal = Proposal.objects.create(
            advert=advert, bidder=self.bidder, message='Teklif', status=Proposal.Status.ACCEPTED
        )
        self.conversation = Conversation.objects.get(proposal=proposal)
        self.contract = Contract.objects.create(
            conversation=self.conversation, created_by=self.owner,
            quantity=1000, unit_price=10, due_date='2026-12-31',
            owner_approved=True, bidder_approved=True,
        )

    def _review_payload(self):
        return {
            'workmanship_score': 5, 'timeliness_score': 4,
            'payment_discipline_score': 5, 'defect_rate_score': 4,
            'comment': 'Güzel iş çıkardı.',
        }

    def test_cannot_review_before_both_sides_mark_completed(self):
        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.post(
            reverse('reviews:review_create', args=[self.contract.pk]), self._review_payload()
        )
        self.assertRedirects(response, reverse('contracts:contract_detail', args=[self.conversation.pk]))
        self.assertEqual(Review.objects.count(), 0)

    def test_owner_can_review_bidder_after_completion(self):
        self.contract.mark_completed_for(self.owner)
        self.contract.mark_completed_for(self.bidder)

        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.post(
            reverse('reviews:review_create', args=[self.contract.pk]), self._review_payload()
        )
        self.assertRedirects(response, reverse('accounts:public_profile', args=[self.bidder.username]))
        review = Review.objects.get(contract=self.contract, reviewer=self.owner)
        self.assertEqual(review.reviewee, self.bidder)

        self.bidder.profile.refresh_from_db()
        self.assertEqual(self.bidder.profile.review_count, 1)
        self.assertEqual(float(self.bidder.profile.avg_workmanship), 5.0)

    def test_cannot_review_twice(self):
        self.contract.mark_completed_for(self.owner)
        self.contract.mark_completed_for(self.bidder)
        Review.objects.create(
            contract=self.contract, reviewer=self.owner, reviewee=self.bidder,
            workmanship_score=5, timeliness_score=5, payment_discipline_score=5, defect_rate_score=5,
        )
        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.post(
            reverse('reviews:review_create', args=[self.contract.pk]), self._review_payload()
        )
        self.assertRedirects(response, reverse('accounts:public_profile', args=[self.bidder.username]))
        self.assertEqual(Review.objects.filter(contract=self.contract, reviewer=self.owner).count(), 1)

    def test_stranger_cannot_review(self):
        self.contract.mark_completed_for(self.owner)
        self.contract.mark_completed_for(self.bidder)
        self.client.login(username='yabanci', password='GucluSifre123!')
        response = self.client.get(reverse('reviews:review_create', args=[self.contract.pk]))
        self.assertEqual(response.status_code, 404)

    def test_new_advert_blocked_until_pending_review_done(self):
        self.contract.mark_completed_for(self.owner)
        self.contract.mark_completed_for(self.bidder)

        self.client.login(username='firma1', password='GucluSifre123!')
        response = self.client.get(reverse('fason_advert:create'))
        self.assertRedirects(response, reverse('contracts:contract_detail', args=[self.conversation.pk]))

        Review.objects.create(
            contract=self.contract, reviewer=self.owner, reviewee=self.bidder,
            workmanship_score=5, timeliness_score=5, payment_discipline_score=5, defect_rate_score=5,
        )
        response = self.client.get(reverse('fason_advert:create'))
        self.assertEqual(response.status_code, 200)
