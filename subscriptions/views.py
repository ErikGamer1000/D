from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages

def subscribe(request):
    if request.method == 'POST':
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
                email = mail.send_mail('Confirmação de inscrição!', body, 'contato@eventif.com.br', ['contato@eventif.com.br', form.cleaned_data['email']])
                messages.success(request, 'Inscrição realizada com sucesso!')
                return HttpResponseRedirect('/inscricao/')
            else:
                 return render(request, 'subscriptions/subscription_form.html', {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)

MESSAGE = '''
Olá! Tudo bem?

Muito obrigado por se inscrever no Eventif.

Estes foram os dados que você enviou na sua
inscrição.

Nome: Cleber Fonseca
CPF: 12345678901
Email: profcleberfonseca@gmail.com
Telefone: 53-12345-6789

Em até 48h úteis alguem da nossa equipe entrará
em contato com você para concluirmos a sua 
inscrição.

Atenciosamente,
Equipe EventIF
'''