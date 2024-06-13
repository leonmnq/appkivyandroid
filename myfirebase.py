import requests  # para fazer requisições na API
from kivy.app import App  # importa a classe App


# classe que gerencia a criação de contas e login
class MyFirebase():
    # API_KEY = "AIzaSyB-vDE1bVma8GvTAiDda7Kg3MXh1GvH75M"
    # API_KEY = "AIzaSyDckbWFrxozXlNFH3AOmAZZEg-4FV61hT0"
    API_KEY = "AIzaSyDsq5ykLGoUpn0LxGfU3NK5mbknIfGnbkw"

    # fonte dos links de autenticação
    # Link do Google REST API para Autenticação = https://cloud.google.com/identity-platform/docs/use-rest-api?hl=pt-br
    def criar_conta(self, email, senha):
        # link para criar conta
        # requisição para a API do Google, que cria o usuário
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        #print(f"email = {email}, senha = {senha}")
        # Payload do corpo da solicitação, informações que precisamos enviar
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dicionario = requisicao.json()
        # print(requisicao_dicionario)

        if requisicao.ok:  # se a requisição deu certo
            #print("Usuário Criado")
            # o que retorna caso o usuário seja criado
            # requisicao_dicionario["kind"]
            # requisicao_dicionario["idToken"] -> autenticação - IMPORTANTE - é o que diz o que o usuário pode alterar e o que ele não pode alterar no banco de dados
            # requisicao_dicionario["email"]
            # requisicao_dicionario["refreshToken"] -> token que mantém o usuário logado - IMPORTANTE - permite que o usuário permaneça logado quando reabrir o aplicativo
            # requisicao_dicionario["expiresIn"] -> em quanto tempo vai expirar o login desse usuário
            # requisicao_dicionario["localId"] -> id_usuario - IMPORTANTE
            refresh_token = requisicao_dicionario["refreshToken"]
            local_id = requisicao_dicionario["localId"]
            id_token = requisicao_dicionario["idToken"]

            meu_aplicativo = App.get_running_app()  # retorna a classe do App que está rodando
            meu_aplicativo.local_id = local_id  # armazena dentro da class MainApp do arquivo main.py o local_id do usuário que estamos pegando
            meu_aplicativo.id_token = id_token

            # with permite trabalhar com arquivos de texto
            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)  # vai criar o arquivo refreshtoken.txt na mesma pasta do projeto, contendo as informações do usuário necessárias para relogar o usuário automaticamente a próxima vez que abrir o app

            # requisição para pegar uma informação do proximo_id_vendedor no banco de dados
            requisicao_id = requests.get(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}")
            requisicao_id_dicionario = requisicao_id.json()
            #print(f"requisicao_id_dicionario = {requisicao_id_dicionario}")
            id_vendedor = requisicao_id.json()

            # atualizando informações do usuário no banco de dados
            link = f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"
            informacao_padrao_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            # informacao_padrao_usuario = '{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": ""}'

            ## NO FIREBASE PRECISAMOS FAZER A REQUISIÇÃO PATCH AO INVÉS DE POST (POST GERARÁ 2 ID PARA O USUÁRIO, DEIXANDO A INFORMAÇÃO CONFUSA NO BANCO DE DADOS, PATCH CRIARÁ DO JEITO CERTO, GERANDO UM ÚNICO ID)
            requisicao_usuario = requests.patch(link, data=informacao_padrao_usuario)

            # atualizar o valor do proximo_id_vendedor no banco de dados
            proximo_id_vendedor = int(id_vendedor) + 1
            informacao_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/.json?auth={id_token}", data=informacao_id_vendedor)

            # executa a função carregar_informacao_usuario do main.py
            meu_aplicativo.carregar_informacao_usuario()

            # leva para homepage
            meu_aplicativo.mudar_tela("homepage")

        else:
            mensagem_erro = requisicao_dicionario["error"]["message"]
            meu_aplicativo = App.get_running_app()  # retorna a classe do App que está rodando
            pagina_login = meu_aplicativo.root.ids["loginpage"]  # para pegar o id de um cara no main.kv, vou utilizar o meu_aplicativo.root.ids passando o id entre colchetes
            #print(mensagem_erro)
            if "INVALID_EMAIL" in mensagem_erro:
                mensagem_erro = "E-MAIL INVÁLIDO"
            if "EMAIL_EXISTS" in mensagem_erro:
                mensagem_erro = "E-MAIL JÁ EXISTE"
            if "MISSING_EMAIL" in mensagem_erro:
                mensagem_erro = "E-MAIL FALTANDO"
            if "MISSING_PASSWORD" in mensagem_erro:
                mensagem_erro = "SENHA FALTANDO"
            if "WEAK_PASSWORD" in mensagem_erro:
                mensagem_erro = "SENHA FRACA: Senha precisa ter pelo menos 6 caracteres"
            pagina_login.ids["mensagem_login"].text = mensagem_erro  # recebe o erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)  # muda a cor do erro para vermelho
        #print(requisicao_dicionario)

    def fazer_login(self, email, senha):
        # link fonte = https://cloud.google.com/identity-platform/docs/use-rest-api?hl=pt-br
        # Fazer login com e-mail/senha
        # requisição para a API do Google, que faz login do usuário
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        # Payload do corpo da solicitação
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dicionario = requisicao.json()

        if requisicao.ok:  # se a requisição deu certo
            # retorna o refresh_token
            refresh_token = requisicao_dicionario["refreshToken"]

            local_id = requisicao_dicionario["localId"]
            id_token = requisicao_dicionario["idToken"]

            meu_aplicativo = App.get_running_app()  # retorna a classe do App que está rodando
            meu_aplicativo.local_id = local_id  # armazena dentro da class MainApp do arquivo main.py o local_id do usuário que estamos pegando
            meu_aplicativo.id_token = id_token

            # salva o refresh_token dentro de um arquivo
            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_informacao_usuario()  # carrega as informações do usuário
            meu_aplicativo.mudar_tela("homepage")  # encaminha ele para a homepage

        else:  # caso a requisição não dê certo
            mensagem_erro = requisicao_dicionario["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            if "INVALID_EMAIL" in mensagem_erro:
                mensagem_erro = "E-MAIL INVÁLIDO"
            if "EMAIL_NOT_FOUND" in mensagem_erro:
                mensagem_erro = "E-MAIL NÃO ENCONTRADO"
            if "MISSING_PASSWORD" in mensagem_erro:
                mensagem_erro = "SENHA FALTANDO"
            if "INVALID_PASSWORD" in mensagem_erro:
                mensagem_erro = "SENHA INVÁLIDA"
            if "INVALID_LOGIN_CREDENTIALS" in mensagem_erro:
                mensagem_erro = "CREDENCIAIS INVÁLIDAS"
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)


    def trocar_token(self, refresh_token):  # função que utiliza o token que estava salvo dentro do arquivo refreshtoken.txt para fazer login automático do usuário, perpetuar usuário
        # link fonte = https://cloud.google.com/identity-platform/docs/use-rest-api?hl=pt-br
        # trocar um token de atualização por um token de ID
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"

        # Payload do corpo da solicitação
        info = {
            "grant_type":  "refresh_token",
            "refresh_token": refresh_token
        }
        requisicao = requests.post(link, data=info)
        requisicao_dicionario = requisicao.json()  # transormar a requisição .json em um dicionário python
        #print(f"requisicao_dicionario (trocar_token) = {requisicao_dicionario}")
        local_id = requisicao_dicionario["user_id"]
        id_token = requisicao_dicionario["id_token"]
        return local_id, id_token  # retorna uma tupla
