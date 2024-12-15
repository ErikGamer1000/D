from django.test import TestCase
from django.core import mail
from datetime import datetime
from contact.forms import ContactForm
from contact.models import Contact

class ContactTestForm(TestCase):
    def setUp(self):
        self.form = ContactForm()

    def test_has_form(self):
        fields = ['name', 'phone', 'email', 'message']
        self.assertSequenceEqual(fields, list(self.form.fields))

class ContactGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/contato/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'contact/contact_form.html')

    def test_html(self):
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('type="text"', 2),
            ('type="email"', 1),
            ('type="submit"', 1),
            ('<textarea', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

class ContactPostValid(TestCase):
    def setUp(self):
        data = dict(name="Erik Pinheiro", phone="53-91234-5678", email="erikmiluk@gmail.com", message="Contato enviado com sucesso.")
        self.resp = self.client.post('/contato/', data)

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)

    def test_send_contact_email(self):
        self.assertEqual(1, len(mail.outbox))

class ContactPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/contato/', {})

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.resp, 'contact/contact_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_form_has_error(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class ContactEmailSent(TestCase):
    def setUp(self):
        data = dict(name="Erik Miluk Pinheiro", email="erikmiluk@gmail.com", phone="53-91234-5678", message="Necessito entrar em contato sobre uma dúvida no evento")
        self.client.post('/contato/', data)
        self.email = mail.outbox[0]

    def test_contact_email_subject(self):
        expect = 'Confirmação de contato!'
        self.assertEqual(expect, self.email.subject)

    def test_contact_email_from(self):
        expect = 'erikmiluk@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_contact_email_to(self):
        expect = ['contato@eventif.com.br', 'erikmiluk@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_contact_email_body(self):
        subjects = (
            'Erik Miluk Pinheiro',
            'erikmiluk@gmail.com',
            '53-91234-5678',
            'Necessito entrar em contato sobre uma dúvida no evento'
        )
        for content in subjects:
            with self.subTest():
                self.assertIn(content, self.email.body) 

class SuccessContactMessage(TestCase):
    def test_success_message(self):
        data = dict(name="Erik Miluk Pinheiro", email="erikmiluk@gmail.com", phone="53-91234-5678", message="Necessito entrar em contato sobre uma dúvida no evento")
        resp = self.client.post('/contato/', data, follow=True)
        self.assertContains(resp, 'Contato enviado')

class ContactModelTest(TestCase):
    def setUp(self):
        self.obj = Contact(
            name = 'Erik Pinheiro',
            email = 'erikmiluk@gmail.com',
            phone = '53-123435-6789',
            message = 'Necessito tirar uma dúvida sobre o evento'        
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Contact.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Erik Pinheiro', str(self.obj))

    def test_flag_default_False(self):
        self.assertEqual(False, self.obj.flag)

    def test_phone_can_be_blank(self):
        field = self.obj._meta.get_field('phone')
        self.assertTrue(field.blank)