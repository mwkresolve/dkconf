Discord para contribuidores : https://discord.gg/UdTc3w4j8f




Projeto de um jogo onde o jogador será um hacker, tera que fazer missoes, instalar virus e gerar dinheiro e bitcoin, deixar seu servidor mais forte,  destruir servidores(bots do jogo e jogadores reais)

## Como utilizar
* Clona repositório
  ```bash
  $ git clone https://github.com/mwkresolve/dkconf.git
  $ cd darkconflicts
  ```
* Preparando o ambiente virtual
  ```bash
  $ python3 -m venv env
  $ source env/bin/activate
  $ pip install -r requirements.txt
  ```
* Roda as migrações
  ```bash
  $ python manage.py migrate
  ```

* Criar superusuario
  ```bash
  $ python manage.py createsuperuser
  ```

* Inicia o servidor
  ```bash
  $ python manage.py runserver
  ```

* Popular o banco de dados com as informações do jogo
  ```bash
  $ acesse http://127.0.0.1:8000/controller e clique em generate game depois generate bots
  ```
Qualquer ajuda é bem vinda :)


