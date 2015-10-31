===============================
Pre requisitos para rodar o app
===============================

-> Ativar virtualenv

source venv/bin/activate

-> Instalar todos as python libraries

pip install -r requirements.txt

=================
Como rodar o app:
=================

==================================================================================================
Estes dois passos a seguir somente deverao ser executado uma vez ou quando o models.py for alterado
==================================================================================================

-> Realizar makemigrations (se necessario futuramente alterar o models.py) e migrate para criar as databases atraves do django
-> *** Posteriormente, caso necessario visualizar o sql gerado pelo django, basta realizar "python manage.py sqlall carroceiro"

python manage.py migrate

-> Carregar dados iniciais no db atraves do script load_catadores.sh

cd scripts
sh load_catadores.sh

-> Inicializar o server

python manage.py runserver

==================================
Como rodar os testes de integracao:
==================================

py.test integration_tests/tests.py

Obs: Como sao testes de integracao, eh necessario que a database esteja existente e funcional (django migrate stuff)

==================================================================================================================
Como Recriar todas as databases do django (caso  necessario algum debug ou destruir as databases por algum motivo):
==================================================================================================================

python manage.py reset_db

-> Posteriormente utilizar

python manage.py migrate

-> Executar novamente o script load_catadores.sh para inicializar data no db.


