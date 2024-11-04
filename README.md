# EventIF

Sistema de evento encomendado pela direção do campus Rio Grande

## Como desenvolver

1. Clonar o repositório.
2. Crie um virtualenv com python 3.10.
3. Ative o seu virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env.
6. Execute os testes.

```console
git clone https://github.com/ErikGamer1000/DS2
cd eventif
python -m venv .eventif
source .eventif/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```