from django.test import TestCase
from django.core import mail
from contact.forms import ContactForm

class ContactTestForm(TestCase):
    def setUp(self):
        self.form = ContactForm()

    def test_has_form(self):
        fields = ['name', 'phone', 'email', 'message']
        self.assertSequenceEqual(fields, list(self.form.fields))

# class ContactPostValid(TestCase):
#     def setUp(self):
#         data = dict(name="Erik Miluk Pinheiro", email="erikmiluk@gmail.com", phone="53-91234-5678", message="Mensagem padrão de envio de contato")
#         self.client.post('/contato/', data)
#         self.email = mail.outbox[0]

#     def test_contact_email_subject(self):
#         expect = 'Confirmação de contato!'
#         self.assertEqual(expect, self.email.subject)

#     def test_contact_email_from(self):
#         expect = 'erikmiluk@gmail.com'
#         self.assertEqual(expect, self.email.from_email)

#     def test_contact_email_to(self):
#         expect = ['contato@eventif.com.br', 'erikmiluk@gmail.com']
#         self.assertEqual(expect, self.email.to)

#     def test_contact_email_body(self):
#         subjects = (
#             'Erik Miluk Pinheiro',
#             'erikmiluk@gmail.com',
#             '53-91234-5678',
#             'Mensagem padrão de envio de contato'
#         )
#         for content in subjects:
#             with self.subTest():
#                 self.assertIn(content, self.email.body)

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