from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.core.models import Speaker


class HomeTest(TestCase):
    def setUp(self):
        Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            photo='http://hbn.link/hopper-pic',
            website='http://hbn.link/hopper-site',
            description='Programadora e almirante.'
        )
        Speaker.objects.create(
            name='Alan Turing',
            slug='alan-turing',
            photo='http://hbn.link/turing-pic',
            website='http://hbn.link/turing-site',
            description='Programador e matemático.'
        )
        self.response = self.client.get(r('home'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        expected = 'href="{}"'.format(r('subscriptions:new'))
        self.assertContains(self.response, expected)

    def test_speakers(self):
        """Must show keynotes speakers"""
        contents = [
            'href="{}"'.format(r('speaker_detail', slug='grace-hopper')),
            'Grace Hopper',
            'http://hbn.link/hopper-pic',
            'href="{}"'.format(r('speaker_detail', slug='alan-turing')),
            'Alan Turing',
            'http://hbn.link/turing-pic',
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_speakers_link(self):
        expected = 'href="{}#speakers"'.format(r('home'))
        self.assertContains(self.response, expected)