# -*- coding:utf-8 -*-
#
# Copyright 2012 NAMD-EMAP-FGV
#
# This file is part of PyPLN. You can get more information at: http://pypln.org/.
#
# PyPLN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyPLN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyPLN.  If not, see <http://www.gnu.org/licenses/>.
from django.core.urlresolvers import reverse

from rest_framework.reverse import reverse as rest_framework_reverse

from pypln.web.core.models import Document
from pypln.web.core.tests.utils import TestWithMongo

__all__ = ["PlainTextVisualizationTest", "FreqDistVisualizationTest"]


class PlainTextVisualizationTest(TestWithMongo):
    fixtures = ['users', 'corpora', 'documents']

    def setUp(self):
        self.document = Document.objects.filter(owner__username="user")[0]
        self.user = self.document.owner

    def test_requires_login(self):
        response = self.client.get(reverse('plain-text-visualization',
            kwargs={'pk': self.document.id}))
        self.assertEqual(response.status_code, 403)

    def test_shows_document_correctly(self):
        self.client.login(username="user", password="user")
        response = self.client.get(reverse('plain-text-visualization',
            kwargs={'pk': self.document.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.renderer_context['view'].object, self.document)
        self.assertEqual(response.data['text'],
                self.document.properties['text'])

    def test_returns_404_for_inexistent_document(self):
        self.client.login(username="user", password="user")
        response = self.client.get(reverse('plain-text-visualization',
            kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_returns_404_if_user_is_not_the_owner_of_the_document(self):
        self.client.login(username="user", password="user")
        document = Document.objects.filter(owner__username="admin")[0]
        response = self.client.get(reverse('plain-text-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 404)

    def test_only_accepts_get(self):
        self.client.login(username="user", password="user")
        document = Document.objects.filter(owner__username="admin")[0]

        response = self.client.post(reverse('plain-text-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 405)

        response = self.client.put(reverse('plain-text-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse('plain-text-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 405)


class FreqDistVisualizationTest(TestWithMongo):
    fixtures = ['users', 'corpora', 'documents']

    def setUp(self):
        self.document = Document.objects.filter(owner__username="user")[0]
        self.user = self.document.owner

    def test_requires_login(self):
        response = self.client.get(reverse('freq-dist-visualization',
            kwargs={'pk': self.document.id}))
        self.assertEqual(response.status_code, 403)

    def test_shows_document_correctly(self):
        self.client.login(username="user", password="user")
        response = self.client.get(reverse('freq-dist-visualization',
            kwargs={'pk': self.document.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.renderer_context['view'].object, self.document)
        self.assertEqual(response.data['freqdist'],
                self.document.properties['freqdist'])

    def test_returns_404_for_inexistent_document(self):
        self.client.login(username="user", password="user")
        response = self.client.get(reverse('freq-dist-visualization',
            kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_returns_404_if_user_is_not_the_owner_of_the_document(self):
        self.client.login(username="user", password="user")
        document = Document.objects.filter(owner__username="admin")[0]
        response = self.client.get(reverse('freq-dist-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 404)

    def test_only_accepts_get(self):
        self.client.login(username="user", password="user")
        document = Document.objects.filter(owner__username="admin")[0]

        response = self.client.post(reverse('freq-dist-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 405)

        response = self.client.put(reverse('freq-dist-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse('freq-dist-visualization',
            kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, 405)
