from django.db import models

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
