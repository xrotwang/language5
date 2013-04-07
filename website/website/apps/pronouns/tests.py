from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun

class Test_PronounParadigmView(TestCase):
    def setUp(self):
        # generate a paradigm.
        # generate a set of pronouns with form set to repr
        pass
        
    def test(self):
        pass
    
    def test_post(self):
        pass




class Test_AddParadigmView(TestCase):
    
    def setUp(self):
        self.url = reverse('pronouns:add')
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.lang = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', 
                                             classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year=1991, author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'pronouns/add.html')
    
    def test_fail_when_not_logged_in(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse("pronouns:add")))
        
    def test_paradigm_save(self):
        count = Paradigm.objects.count()
        response = self.client.post(self.url, {
            'language': self.lang.id, 'source': self.source.id, 'comment': 'foo'
        }, follow=True)
        self.assertEqual(Paradigm.objects.count(), count+1)
        self.assertContains(response, 'foo')
        
    def test_paradigm_creates_pronouns(self):
        count = Pronoun.objects.count()
        response = self.client.post(self.url, {
            'language': self.lang.id,
            'source': self.source.id,
            'comment': 'foo'
        }, follow=True)
        self.assertEqual(Pronoun.objects.count(), count+len(Pronoun._generate_all_combinations()))
        