from django.test import TestCase
from django.urls import reverse

from .models import User, Profile, Document, DocumentAccessRequest


class UserRegistrationTests(TestCase):
    def test_register_creates_profile_automatically(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'atolye1',
            'email': 'atolye1@example.com',
            'first_name': 'Test',
            'last_name': 'Atolye',
            'role': User.Role.WORKSHOP,
            'phone': '05551112233',
            'city': 'İstanbul',
            'company_name': 'Test Atölyesi',
            'password1': 'GucluSifre123!',
            'password2': 'GucluSifre123!',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='atolye1')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.company_name, 'Test Atölyesi')


class VerificationBadgeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='atolye2', password='GucluSifre123!', role=User.Role.WORKSHOP
        )

    def test_uploading_tax_certificate_verifies_profile(self):
        profile = self.user.profile
        self.assertFalse(profile.is_verified)

        Document.objects.create(
            user=self.user,
            document_type=Document.DocumentType.TAX_CERTIFICATE,
            file='documents/test.pdf',
        )

        profile.refresh_from_db()
        self.assertTrue(profile.is_verified)
        self.assertIsNotNone(profile.verified_at)

    def test_deleting_tax_certificate_removes_badge(self):
        profile = self.user.profile
        doc = Document.objects.create(
            user=self.user,
            document_type=Document.DocumentType.TAX_CERTIFICATE,
            file='documents/test.pdf',
        )
        profile.refresh_from_db()
        self.assertTrue(profile.is_verified)

        doc.delete()
        profile.refresh_from_db()
        self.assertFalse(profile.is_verified)

    def test_id_copy_alone_does_not_verify(self):
        profile = self.user.profile
        Document.objects.create(
            user=self.user,
            document_type=Document.DocumentType.ID_COPY,
            file='documents/kimlik.pdf',
        )
        profile.refresh_from_db()
        self.assertFalse(profile.is_verified)


class DocumentAccessRequestTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='atolye_sahibi', password='GucluSifre123!', role=User.Role.WORKSHOP)
        self.viewer = User.objects.create_user(username='firma_sahibi', password='GucluSifre123!', role=User.Role.CUSTOMER)
        self.document = Document.objects.create(
            user=self.owner,
            document_type=Document.DocumentType.ID_COPY,
            file='documents/kimlik.pdf',
        )

    def test_viewer_cannot_see_document_without_approval(self):
        self.client.login(username='firma_sahibi', password='GucluSifre123!')
        response = self.client.get(reverse('accounts:public_profile', args=['atolye_sahibi']))
        self.assertContains(response, 'Görüntüleme İsteği Gönder')
        self.assertNotContains(response, 'kimlik.pdf')

    def test_request_then_approve_allows_view_button(self):
        self.client.login(username='firma_sahibi', password='GucluSifre123!')
        self.client.post(reverse('accounts:document_request_access', args=[self.document.pk]))

        access_request = DocumentAccessRequest.objects.get(document=self.document, requester=self.viewer)
        self.assertEqual(access_request.status, DocumentAccessRequest.Status.PENDING)

        self.client.logout()
        self.client.login(username='atolye_sahibi', password='GucluSifre123!')
        self.client.post(reverse('accounts:document_request_approve', args=[access_request.pk]))

        access_request.refresh_from_db()
        self.assertEqual(access_request.status, DocumentAccessRequest.Status.APPROVED)

    def test_owner_can_deny_request(self):
        self.client.login(username='firma_sahibi', password='GucluSifre123!')
        self.client.post(reverse('accounts:document_request_access', args=[self.document.pk]))
        access_request = DocumentAccessRequest.objects.get(document=self.document, requester=self.viewer)

        self.client.logout()
        self.client.login(username='atolye_sahibi', password='GucluSifre123!')
        self.client.post(reverse('accounts:document_request_deny', args=[access_request.pk]))

        access_request.refresh_from_db()
        self.assertEqual(access_request.status, DocumentAccessRequest.Status.DENIED)

    def test_non_owner_cannot_respond_to_request(self):
        self.client.login(username='firma_sahibi', password='GucluSifre123!')
        self.client.post(reverse('accounts:document_request_access', args=[self.document.pk]))
        access_request = DocumentAccessRequest.objects.get(document=self.document, requester=self.viewer)

        # viewer (istek sahibi, ama belge sahibi değil) onaylamaya çalışıyor
        response = self.client.post(reverse('accounts:document_request_approve', args=[access_request.pk]))
        self.assertEqual(response.status_code, 404)
