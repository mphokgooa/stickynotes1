from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Note
from .forms import NoteForm

User = get_user_model()

class NoteModelTest(TestCase):
    def test_create_note_model(self):
        user = User.objects.create_user(username='tester', password='pass')
        n = Note.objects.create(title='Test Note', content='Content', owner=user)
        self.assertEqual(str(n), 'Test Note')
        self.assertEqual(Note.objects.count(), 1)

class NoteFormTest(TestCase):
    def test_note_form_validation(self):
        form = NoteForm({'title': '  ', 'content': 'x'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_note_form_valid(self):
        form = NoteForm({'title': 'Hello', 'content': 'World'})
        self.assertTrue(form.is_valid())

class NoteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewer', password='pass')
        self.note = Note.objects.create(title='Note1', content='Content1', owner=self.user)

    def test_index_view(self):
        resp = self.client.get(reverse('notes:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'notes/index.html')

    def test_create_requires_login(self):
        resp = self.client.get(reverse('notes:note_create'))
        self.assertEqual(resp.status_code, 302)  # redirects to login

    def test_create_note_post(self):
        self.client.login(username='viewer', password='pass')
        resp = self.client.post(reverse('notes:note_create'), {'title':'New','content':'Body'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Note.objects.filter(title='New').count(), 1)
