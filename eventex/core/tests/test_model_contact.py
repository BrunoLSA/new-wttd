from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Bruno Santana',
            slug='bruno-santana',
            photo='http://hbn.link/bs-pic'
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                                         value='santanasta@gmail.com')
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE,
                                         value='92-994104333')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contac kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL,
                          value='santanasta@gmail.com')
        self.assertEqual('santanasta@gmail.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Bruno Santana',
            slug='bruno-santana',
            photo='http://hbn.link/bs-pic'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='santanasta@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='92-994104333')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['santanasta@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['92-994104333']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)