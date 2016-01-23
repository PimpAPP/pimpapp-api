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

Estes dois passos a seguir somente deverao ser executado uma vez ou quando o models.py for alterado

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

py.test integration_tests/tests.py -v

Obs: Como sao testes de integracao, eh necessario que a database esteja existente e funcional (django migrate stuff)

Veja a sessao de autenticacao antes de rodar os testes!

=================================
Autenticacao
==================================

Todos os metodos de escrita, e.g, PUT/DELETE/POST estao protegidos por Token Authentication.

Existe uma database que o django cria automaticamente (apos um manage.py migrate) e devido ao arquivo signals.py cada usuario criado atraves
do manage.py createsuperuser ira associar um token para este usuario.

Entao para autenticar basta enviar qualquer token de qualquer usuario que existe nesta database. No caso deste app, partimos do pressuposto que ira
existir somente um admin (pode existir mais se necessario sem problemas), entao eh necessario criar somente um usuario com nome qualquer (pimpapp por ex) e este ira ter um token.
Posteriormente, qualquer requisicao de REST PUT/DELETE/POST somente ira ser autorizada caso o token exista na database.

***Importante***

Como os testes fazem utilizacao da autenticacao, eh necessario que o token utilizado nos metodos seja correto, ou em outras palavras exista na nossa database.
Entao, antes de executar os testes, faca o set da variavel global token com o mesmo valor do token que existe no database que foi gerado apos a criacao do usuario no arquivo tests.py
{ara saber qual o token do usuario criado, basta entrar em "127.0.0.1:8000/admin" e visualizar a tabela AuthToken/Tokens. Ou fazer um select nesta tabela atraves do CLI usando o slqlite por exemplo.

No arquivo README.md existe um exemplo com curl e token authentication, para fazer um teste manual, se necessario.

==================================================================================================================
Como Recriar todas as databases do django (caso  necessario algum debug ou destruir as databases por algum motivo):
==================================================================================================================

python manage.py reset_db

-> Posteriormente utilizar

python manage.py migrate

-> Executar novamente o script load_catadores.sh para inicializar data no db.

===============

Observações de um iniciante em djnago e sqlite após seguir o procedimento:

Para criação do virtualenv com Python 3.4:
virtualenv -p /usr/bin/python3.4 venv

Ir para o diretório app_site antes do comando migrate

Instalar sqlite3 para rodar script load_carroceiros.sh
Pode-se usar o comando: apt-get install sqlite3

Se necessário, dar permissão de escrita no arquivo do banco de dados: db.sqlite3.

Dentro do sqlite3, usar:
.help para ver comandos existentes
.open <nome do banco de dados> - app_site/db.sqlite3
.databases para ver bases de dados
.tables <tabela> para ver todas as tabelas ou uma tabela específica
.dump <tabela> para ver dados de todas as tabelas ou uma tabela específica

Criar usuário administrador para acessar Administração do Site / Administração do Django, com o comando:
python manage.py createsuperuser

Com este usuário logar em <sua máquina>:<sua porta>/admin - 127.0.0.1:8000/admin, conforme descrito no item "Autenticação", tópico "Importante".
