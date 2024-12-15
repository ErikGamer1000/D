from django.db import models
from django.core import mail
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Contact(models.Model):
    name = models.CharField('nome', max_length=100)
    email = models.EmailField('e-mail')
    phone = models.CharField('telefone', max_length=20, blank=True)
    message = models.CharField('mensagem', max_length=100)
    created_at = models.DateTimeField('enviado em', auto_now_add=True)
    response = models.CharField('response', max_length=20, null=True)
    responsed_at = models.DateTimeField('respondido em', null=True)
    flag = models.BooleanField('respondido', default=False)

    class Meta:
        verbose_name_plural = 'Contatos'
        verbose_name = 'contato'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Contact)
def my_handler(sender, instance, **kwargs):
    if instance.response != "":
        _send_mail('contact/contact_response.txt', 
            vars(instance), 
            'Confirmação de resposta!', 
            instance.email,
            settings.DEFAULT_FROM_EMAIL)
        responsed_at = now()
        flag = True



def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    email = mail.send_mail(subject, body, from_, [from_, to])