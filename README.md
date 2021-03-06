[![Build Status](https://travis-ci.org/PimpAPP/pimpapp-api.svg?branch=master)](https://travis-ci.org/PimpAPP/pimpapp-api)

# Cataki API

Esse é o projeto back-end do aplicativo [Cataki](http://www.cataki.org).  
Ele fornece a API utilizada pelo [projeto mobile](https://github.com/PimpAPP/pimpapp-mobile).

## Tecnologias Utilizadas

- [Django](https://www.djangoproject.com/)
- [Djago Rest Framework](http://www.django-rest-framework.org/)

## Configuração do Projeto

Obs: O manual a seguir irá mencionar o arquivo `manage.py` várias. Ele encontra-se dentro da pasta `app_site`, então certifique-se de estar nessa pasta antes de rodar os comandos que envolvem o `manage.py`.

### Pré-Requisitos

Você deve ter os seguintes pacotes instalados em seu computador:

- [Git](https://git-scm.com/)
- [Python 3.x](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

### Configuração do Ambiente

Dentro da pasta do projeto, crie um virtualenv e ative-o:

```shell
virtualenv --python=python3 venv
source venv/bin/activate
```

Instale as dependências:
```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Obs: Em caso de erro, pode ser que esteja faltando algum pacote no sistema do qual dependemos. Cheque o item abaixo, `Dependências do Sistema`, e instale as dependências listadas, depois tente novamente rodar os comandos acima.

#### Dependências do Sistema
O pacote Pillow depende das seguintes bibliotecas:

- libjpeg: provides JPEG functionality.
- zlib: provides access to compressed PNGs
- libtiff: provides group4 tiff functionality
- libfreetype: provides type related services
- littlecms: provides color management
- libwebp: provides the Webp format

As instruções exatas de instalação delas vão depender do sistema operacional/distribuição que você utiliza.

##### Debian/Ubuntu
Na maquina debian do DigitalOcean os pacotes necessários foram libjpeg-dev e zlib1g-dev

```shell
apt-get install libjpeg-dev zlib1g-dev
```

### Banco de Dados

#### Migrações

Você deve criar e rodar as migrações para que as tabelas sejam criadas no seu banco de dados local.

```sh
python manage.py makemigrations
pythos manage.py makemigrations api
python manage.py migrate
```

#### Dados

*-- DEPRECATED --* Não temos no momento uma dump de dados atualizado para uso em desenvolvimento

Carregar dados iniciais no db atraves do script `load_catadores.sh`.

[//]: # (TODO Esse script não existe)

```sh
cd scripts
sh load_catadores.sh
```

[//]: # (TODO Escrever sobre o local_settings.py)

## Desenvolvendo

Para rodar o servidor local:

```sh
python manage.py runserver
```

#### Criando migrações

Sempre que houver alterações nos models que devam ser refletidas no banco de dados, deve-se rodar o comando `makemigrations` para criar as migrações necessárias.

```sh
python manage.py makemigrations
```

Caso seja necessário visualizar o sql gerado pelo django para uma determinada migração:

```sh
python manage.py sqlmigrate api <migration_name>
 ```

#### Resetando o Banco
Caso você precise resetar o banco e recriar as tabelas do zero, rode o seguinte comando (isso irá deletar todos os dados no banco):

```sh
python manage.py reset_db
```

Depois rode novamente as migrações:

```sh
python manage.py migrate
```

### Testes

#### Como rodar os testes de integração

```sh
py.test integration_tests/tests.py -v
```

Obs: Como são testes de integração, é necessário que a database esteja existente e funcional (django migrate stuff)

Veja a sessão de autenticação antes de rodar os testes!

### Autenticação

Todos os metodos de escrita, e.g, PUT/DELETE/POST estão protegidos por Token Authentication.

Existe uma database que o django cria automaticamente (após um manage.py migrate) e devido ao arquivo signals.py cada usuário criado através
do manage.py createsuperuser irá associar um token para este usuário.

Então para autenticar basta enviar qualquer token de qualquer usuário que existe nesta database. No caso deste app, partimos do pressuposto que irá
existir somente um admin (pode existir mais se necessário sem problemas), então é necessário criar somente um usuário com nome qualquer (pimpapp por ex) e este irá ter um token.
Posteriormente, qualquer requisição de REST PUT/DELETE/POST somente irá ser autorizada caso o token exista na database.

***Importante***

Como os testes fazem utilização da autenticação, é necessário que o token utilizado nos métodos seja correto, ou em outras palavras exista na nossa database.
Então, antes de executar os testes, faça o set da variável global token com o mesmo valor do token que existe no database que foi gerado após a criação do usuário no arquivo tests.py
Para saber qual o token do usuário criado, basta entrar em "127.0.0.1:8000/admin" e visualizar a tabela AuthToken/Tokens. Ou fazer um select nesta tabela através do CLI usando o slqlite por exemplo.

No arquivo README.md existe um exemplo com curl e token authentication, para fazer um teste manual, se necessário.

### Observações de um iniciante em django e sqlite após seguir o procedimento:

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
