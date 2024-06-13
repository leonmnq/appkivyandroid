# a parte lógica vai ser criada em .py e a parte visual vai ser criada em .kv
# sempre inicia o aplicativo com um main.py e um main.kv

from kivy.app import App  # biblioteca para criação de aplicativos mobile em python
from kivy.lang import Builder  # é quem vai conectar o arquivo .kv com o arquivo .py
from kivy.uix.screenmanager import Screen  # classe Screen cria telas
from telas import *  # importa todas as classes do arquivo telas.py
from botoes import *  # importa todas as classes do botoes.py
import requests  # para poder fazer requesições no banco de dados
from bannervenda import BannerVenda  # importa a classe BannerVenda
import os  # para lidar com arquivos do computador
from functools import partial  # o partial permite que você passe um parâmetro para uma função que está sendo usada como parâmetro para o botão
from myfirebase import MyFirebase  # importa a classe MyFirebase
from bannervendedor import BannerVendedor  # importa a classe BannerVendedor
from datetime import date  # para pegar a data atual

GUI = Builder.load_file("main.kv")  # a interface gráfica será Builder.load_file("main.kv")


class MainApp(App):  # classe MainApp é uma subclasse da classe App
    # id_usuario = 1  # teste para abrir informação do usuário 1 assim que rodar o app
    cliente = None  # para utilizar na função adicionar_venda()
    produto = None  # para utilizar na função adicionar_venda()
    unidade = None  # para utilizar na função adicionar_venda()

    def build(self):  # constrói o aplicativo
        self.firebase = MyFirebase()  # uma instância da classe MyFirebase
        return GUI

    def on_start(self):  # função que executa assim que o app inicia
        # carregar as fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")  # lista todos os arquivos do diretório icones/fotos_perfil
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        lista_fotos = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            print(f"foto = {foto}")
            # imagem = Image(source=f"icones/fotos_perfil/{foto}")
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        # carregar as fotos dos clientes (MERCADOS)
        arquivos = os.listdir("icones/fotos_clientes")  # lista todos os arquivos do diretório icones/fotos_clientes
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]
        for foto_cliente in arquivos:
            print(f"foto_cliente = {foto_cliente}")
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}",
                                 on_release=partial(self.selecionar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace(".png", "").capitalize(),  # tira .png do nome e coloca a primeira letra maiúscula (capitalize())
                                on_release=partial(self.selecionar_cliente, foto_cliente))  # no partial é passada a função que queremos e o parâmetro que vamos enviar para aquela função
            lista_clientes.add_widget(imagem)  # adiciona a imagem na lista
            lista_clientes.add_widget(label)  # adiciona o rótulo na lista

        # carregar as fotos dos produtos
        arquivos = os.listdir("icones/fotos_produtos")  # lista todos os arquivos do diretório icones/fotos_produtos
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}",
                                 on_release=partial(self.selecionar_produto, foto_produto))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_produto, foto_produto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        # carregar a data (pega a data de hoje)
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        label_data = pagina_adicionarvendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"

        # carrega as infos do usuario
        self.carregar_informacao_usuario()

    def carregar_informacao_usuario(self):
        try:  # tenta carregar as informações do usuário

            # para fazer login automaticamente para um usuário que saiu e voltou para o aplicativo
            # se existir o arquivo refreshtoken.txt, vai lê-lo e armazenar a informação na variável refresh_token
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()

            # chama a função trocar_token do myfirebase.py passando refresh_token como parâmetro
            local_id, id_token = self.firebase.trocar_token(refresh_token)  # retornar uma tupla
            self.local_id = local_id
            self.id_token = id_token

            # pegar informações do usuario
            # requisicao = requests.get(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.id_usuario}.json")
            requisicao = requests.get(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}")  # a requisição deve terminar com .json  # '?auth={self.id_token}' diz quem é o usuário que está fazendo essa requisição
            # sempre que é feita uma requisição, ela é devolvida para nós no formato json
            print(f"requisicao.json() = {requisicao.json()}")  # colocando .json() aqui, a informação retorna traduzida em um dicionário python
            requisicao_dicionario = requisicao.json()

            # preencher foto de perfil
            avatar = requisicao_dicionario['avatar']
            print(avatar)
            self.avatar = avatar  # vai me permitir armazenar dentro do MainApp, dentro do self, as informações desse usuário, não sendo necessário fazer requisição toda hora
            foto_perfil = self.root.ids["foto_perfil"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"  # atualiza com a foto de perfil do usuário
            print(f"requisicao_dicionario['vendas'] = {requisicao_dicionario['vendas']}")

            # preencher o ID único
            id_vendedor = requisicao_dicionario['id_vendedor']
            self.id_vendedor = id_vendedor  # vai me permitir armazenar dentro do MainApp, dentro do self, as informações desse usuário, não sendo necessário fazer requisição toda hora
            pagina_ajustes = self.root.ids["ajustespage"] # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID Único: {id_vendedor}"

            # preencher o total de vendas
            total_vendas = requisicao_dicionario['total_vendas']
            self.total_vendas = total_vendas  # vai me permitir armazenar dentro do MainApp, dentro do self, as informações desse usuário, não sendo necessário fazer requisição toda hora
            homepage = self.root.ids["homepage"] # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R$ {total_vendas}[/b]"

            # preencher equipe
            self.equipe = requisicao_dicionario["equipe"]  # vai me permitir armazenar dentro do MainApp, dentro do self, as informações desse usuário, não sendo necessário fazer requisição toda hora

            # preencher lista de vendas
            try:
                print(f"requisicao_dicionario (carregar_informacao_usuario) = {requisicao_dicionario}")
                # vendas = requisicao_dicionario['vendas'][1:]
                vendas = requisicao_dicionario['vendas']
                self.vendas = vendas  # vai me permitir armazenar dentro do MainApp, dentro do self, as informações desse usuário, não sendo necessário fazer requisição toda hora
                pagina_homepage = self.root.ids["homepage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
                print(f"pagina_homepage.ids = {pagina_homepage.ids}")
                lista_vendas = pagina_homepage.ids["lista_vendas"]

                # for venda in vendas: # sempre que você tiver que criar um cara de forma dinâmica, você vai ter que criar um elemento dentro do seu arquivo .kv por meio do código em python
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    print(f"venda = {venda}")
                    # venda['cliente']
                    # venda['data']

                    # criando o banner de cada venda
                    # segunda etapa para criação do banner, passar as colunas com as informações das vendas para uma classe BannerVenda que criaremos
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda['data'], preco=venda['preco'],
                                         unidade=venda['unidade'], quantidade=venda["quantidade"])

                    lista_vendas.add_widget(banner)  # adicionando um item na minha lista de vendas
            # except:
            #     pass
            except Exception as excecao:
                print(f"exceção = {excecao}")  # printa a mensagem de erro se existir erro dentro do try

            # preencher equipe de vendedores
            equipe = requisicao_dicionario["equipe"]
            lista_equipe = equipe.split(",")  # lista_equipe recebe uma lista com os valores da coluna equipe separados pelas vírgulas
            pagina_listavendedores = self.root.ids["listarvendedorespage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]

            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":  # se id_vendedor_equipe é diferente de vazio
                    # vamos criar um banner para cada vendedor que existir na equipe
                    banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)
            print("teste")
            self.mudar_tela("homepage")

        except:  # se não der certo carregar as informações do usuário
            pass

    def mudar_tela(self, id_tela):
        print(f"id_tela = {id_tela}")
        print(f"self.root.ids = {self.root.ids}")  # self.root faz referência ao gerenciador de telas, main.kv
        gerenciador_telas = self.root.ids["screen_manager"]  # variável gerenciador_telas recebe o gerenciar de telas
        gerenciador_telas.current = id_tela  # tela atual que será exibida

    def mudar_foto_perfil(self, foto, *args):
        print(f"foto = {foto}")
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        info = f'{{"avatar": "{foto}"}}'  # é necessário passar o texto dessa forma para o banco de dados
        # requisicao = requests.patch(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.id_usuario}.json", data=info)
        # editando as informações do usuário no banco de dados
        requisicao = requests.patch(
            f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
            data=info
        )

        self.mudar_tela("ajustespage")  # retorna para página de ajustes

    def adicionar_vendedor(self, id_vendedor_adicionado):
        # puxar informações do vendedor do banco de dados
        # a interrogação no link "?" significa que a partir dali serão parâmetros, e cada parâmetro é separado por "&"
        link = f'https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'

        # requisição no banco para procurar se tem um vendedor que tem esse mesmo id vendedor
        requisicao = requests.get(link)
        requisicao_dicionario = requisicao.json()
        print(f"requisicao_dicionario (adicionar_vendedor)= {requisicao_dicionario}")

        pagina_adicionarvendedor = self.root.ids["adicionarvendedorpage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        mensagem_texto = pagina_adicionarvendedor.ids["mensagem_outrovendedor"]

        if requisicao_dicionario == {}:  # se requisição_dicionario é um dicionário vazio
            mensagem_texto.text = "Usuário não encontrado"
        else:
            lista_equipe = self.equipe.split(",")  # lista_equipe recebe uma lista com os valores da coluna equipe separados pelas vírgulas
            if id_vendedor_adicionado in lista_equipe:  # se o id do cara que estou tentando adicionar faz parte da equipe
                mensagem_texto.text = "Vendedor já faz parte da equipe"
            else:  # caso não faça parte da equipe
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"  # self.equipe concatenando com vírgula e o id_vendedor_adicionado
                info = f'{{"equipe": "{self.equipe}"}}'  # esse procedimento para transformar em texto
                # atualizando informação do usuário no banco de dados
                requests.patch(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                               data=info)
                mensagem_texto.text = "Vendedor Adicionado com Sucesso"

                # adicionar um novo banner na lista de vendedores
                pagina_listavendedores = self.root.ids["listarvendedorespage"]
                lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)

    def selecionar_cliente(self, foto, *args):  # o *args servirá apenas para permitir a entrada dos demais parâmetros que não utilizaremos para que não ocorra um erro entre a quantidade de parâmetros que são enviados e a quantidade que são recebidos
        self.cliente = foto.replace(".png", "")  # para utilizar na função adicionar_venda()
        # pintar de branco todas as outras letras
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]

        for item in list(lista_clientes.children):  # pega todos os itens que tem dentro da lista_clientes
            item.color = (1, 1, 1, 1)  # pinta todos de branco
            # pintar de azul a letra do item que selecionamos
            # foto -> carrefour.png / Label -> Carrefour -> carrefour -> carrefour.png
            try:  # tenta
                texto = item.text  # pegar o texto do item
                texto = texto.lower() + ".png"  # transforma o texto em letras minúsculas e concatena .png
                if foto == texto:  # se o texto da foto é igual ao texto da variável texto
                    item.color = (0, 207/255, 219/255, 1)  # pinta esse item de azul
            except:
                pass

    def selecionar_produto(self, foto, *args):
        self.produto = foto.replace(".png", "")  # para utilizar na função adicionar_venda()
        # pintar de branco todas as outras letras
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]

        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul a letra do item que selecionamos
            try:  # tenta
                texto = item.text  # pegar o texto do item
                texto = texto.lower() + ".png"  # transforma o texto em letras minúsculas e concatena .png
                if foto == texto:  # se o texto da foto é igual ao texto da variável texto
                    item.color = (0, 207/255, 219/255, 1)  # pinta esse item de azul
            except:
                pass

    def selecionar_unidade(self, id_label, *args):
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        self.unidade = id_label.replace("unidades_", "")  # para utilizar na função adicionar_venda()

        # pintar de branco todas as outras unidades
        pagina_adicionarvendas.ids["unidades_kg"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["unidades_unidades"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["unidades_litros"].color = (1, 1, 1, 1)

        # pintar o cara selecionado de azul
        pagina_adicionarvendas.ids[id_label].color = (0, 207/255, 219/255, 1)

    def adicionar_venda(self):
        cliente = self.cliente  # recebe a seleção que vem da função selecionar_cliente
        produto = self.produto  # recebe a seleção que vem da função selecionar_produto
        unidade = self.unidade  # recebe a seleção que vem da função selecionar_unidade

        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        data = pagina_adicionarvendas.ids["label_data"].text.replace("Data: ", "")  # 11/06/2024
        preco = pagina_adicionarvendas.ids["preco_total"].text
        quantidade = pagina_adicionarvendas.ids["quantidade"].text

        if cliente:  # se cliente foi selecionado
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 1, 1, 1)  # pinta de branco
        if produto:  # se produto foi selecionado
            pagina_adicionarvendas.ids["label_selecione_produto"].color = (1, 1, 1, 1)  # pinta de branco
        if preco:  # se o preço foi selecionado
            pagina_adicionarvendas.ids["label_preco"].color = (1, 1, 1, 1)  # pinta de branco
        if quantidade:  # se quantidade foi selecionada
            pagina_adicionarvendas.ids["label_quantidade"].color = (1, 1, 1, 1)  # pinta de branco

        if not cliente:  # se cliente não foi selecionado
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)  # pinta de vermelho o texto Selecione o cliente
        if not produto:  # se produto não foi selecionado
            pagina_adicionarvendas.ids["label_selecione_produto"].color = (1, 0, 0, 1)  # pinta de vermelho o texto Selecione o produto
        if not unidade:  # se nenhuma unidade foi selecionada
            pagina_adicionarvendas.ids["unidades_kg"].color = (1, 0, 0, 1)  # pinta de vermelho o texto kg
            pagina_adicionarvendas.ids["unidades_unidades"].color = (1, 0, 0, 1)  # pinta de vermelho o texto unidades
            pagina_adicionarvendas.ids["unidades_litros"].color = (1, 0, 0, 1)  # pinta de vermelho o texto litros
        if not preco:  # se o preço não foi selecionado
            pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)  # pinta de vermelho o texto Preço Total
        else:
            try:  # tenta transformar o preço que o usuário digitou em float
                preco = float(preco)
            except:  # se não foi possível, pinta de vermelho
                pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)
        if not quantidade:  # se quantidade não foi selecionada
            pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)  # pinta de vermelho o texto Quantidade
        else:
            try:  # tenta transformar a quantidade que o usuário digitou em float
                quantidade = float(quantidade)
            except:  # se não foi possível, pinta de vermelho
                pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)

        # dado que ele preencheu tudo, vamos executar o código de adicionar venda
        if cliente and produto and unidade and preco and quantidade and (type(preco) == float) and (type(quantidade)==float):
            foto_produto = produto + ".png"  # pega a foto do produto selecionado
            foto_cliente = cliente + ".png"  # pega a foto do cliente selecionado

            # criando a venda
            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}", ' \
                   f'"foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", ' \
                   f'"preco": "{preco}", "quantidade": "{quantidade}"}}'
            # modificando informações do usuário no banco de dados
            requests.post(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}",
                          data=info)

            # criando o banner de venda
            banner = BannerVenda(cliente=cliente, produto=produto, foto_cliente=foto_cliente, foto_produto=foto_produto,
                                 data=data, preco=preco, quantidade=quantidade, unidade=unidade)
            pagina_homepage = self.root.ids["homepage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner)

            # atualizando o total de vendas no banco de dados
            # pegando informações do usuário do banco de dados
            requisicao = requests.get(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}")
            requisicao_dicionario = requisicao.json()
            print(f"requisicao_dicionario (adicionar_venda) = {requisicao_dicionario}")
            total_vendas = float(requisicao.json())
            total_vendas = total_vendas + preco
            info = f'{{"total_vendas": "{total_vendas}"}}'
            # atualizando informações do usuário no banco de dados
            requests.patch(f"https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                           data=info)

            # atualizar o total de vendas no aplicativo
            homepage = self.root.ids["homepage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

            # redireciona para homepage
            self.mudar_tela("homepage")


            # para resetar a seleção
            self.cliente = None
            self.produto = None
            self.unidade = None

    def carregar_todas_vendas(self):
        # manipular o id todasvendaspage
        pagina_todasvendas = self.root.ids["todasvendaspage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        lista_vendas = pagina_todasvendas.ids["lista_vendas"]  # pega a lista de vendas da página totalvendaspage

        # for para verificar se a lista de vendas já existe na página todasvendaspage (para evitar o bug da lista aumentar toda vez que entra na página)
        for item in list(lista_vendas.children):  # para cada item que está dentro da nossa lista de vendas # children significa os itens que estão dentro da lista de vendas
            lista_vendas.remove_widget(item)  # remove esse item

        # preencher a pagina todasvendaspage.kv
        # pegar informações da empresa
        # lendo informações no banco de dados
        requisicao = requests.get(f'https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')  # pegando todas as informações do banco de dados ordenando pelo id_vendedor
        requisicao_dicionario = requisicao.json()
        print(f"requisicao_dicionario (carregar_todas_vendas) = {requisicao_dicionario}")

        # preencher foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        foto_perfil.source = f"icones/fotos_perfil/hash.png"  # preenche com a logo da hashtag

        # preencher lista de vendas
        total_vendas = 0  # 'seta' o total de vendas como zero
        for local_id_usuario in requisicao_dicionario:  # para cada usuário em requisicao_dicionario
            try:  # tenta pegar as vendas desse usuário
                vendas = requisicao_dicionario[local_id_usuario]["vendas"]  # 'vendas' recebe as vendas do usuário
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    # venda["cliente"]
                    total_vendas = total_vendas + float(venda["preco"])  # vai somando o preço de cada venda na variável total_vendas
                    # criando o banner de cada venda
                    banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"], foto_cliente=venda["foto_cliente"],
                                         foto_produto=venda["foto_produto"], data=venda["data"],
                                         preco=venda["preco"], quantidade=venda["quantidade"], unidade=venda["unidade"])
                    lista_vendas.add_widget(banner)  # adiciona o banner na lista de vendas
            except Exception as excecao:
                print(f"exceção (carregar_todas_vendas) = {excecao}")  # printa a mensagem de erro se existir erro dentro do try
        # preencher o total de vendas
        pagina_todasvendas.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R$ {total_vendas}[/b]"  # edita o texto do label_total_vendas da página todasvendaspage

        # redirecionar pra pagina todasvendaspage
        self.mudar_tela("todasvendaspage")

    def sair_todas_vendas(self, id_tela):
        foto_perfil = self.root.ids["foto_perfil"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"  # 'devolve' a foto de perfil do usuário armazenada no self.avatar

        # self.mudar_tela("ajustespage")  # redireciona para página ajustespage
        self.mudar_tela(id_tela)

    def carregar_vendas_vendedor(self, dicionario_informacoes_vendedor, *args):  # passando o parâmetro *args apenas para não dar bug no código

        # Exemplo de  informações que vem no dicionario_informacoes_vendedor:
        # dicionario_informacoes_vendedor = "valor (BannerVendedor)= {'avatar': 'foto12.png', 'equipe': '1,2,3', 'id_vendedor': '4', 'total_vendas': '23.0', 'vendas': {'-O-9Lb2FUBUXIpo4B2o8': {'cliente': 'carrefour', 'data': '11/06/2024', 'foto_cliente': 'carrefour.png', 'foto_produto': 'arroz.png', 'preco': '15.0', 'produto': 'arroz', 'quantidade': '1.0', 'unidade': 'kg'}, '-O-9UxS_Sliy6W2Fu-Xe': {'cliente': 'mundial', 'data': '12/06/2024', 'foto_cliente': 'mundial.png', 'foto_produto': 'feijao.png', 'preco': '8.0', 'produto': 'feijao', 'quantidade': '1.0', 'unidade': 'kg'}}}"

        try:  # tenta
            vendas = dicionario_informacoes_vendedor["vendas"]  # recebe as vendas que vem do dicionario
            pagina_vendasoutrovendedor = self.root.ids["vendasoutrovendedorpage"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
            # pega o id do GridLayout da página vendasoutrovendedorpage
            lista_vendas = pagina_vendasoutrovendedor.ids["lista_vendas"]

            # limpar vendas anteriores
            # for para verificar se a lista de vendas já existe na página vendasoutrovendedorpage (para evitar o bug da lista aumentar toda vez que entra na página com um vendedor que possui vendas)
            for item in list(lista_vendas.children):  # para cada item que está dentro da nossa lista de vendas # children significa os itens que estão dentro da lista de vendas
                lista_vendas.remove_widget(item)  # remove esse item

            for id_venda in vendas:
                venda = vendas[id_venda]
                # criando o banner de cada venda
                banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"], foto_cliente=venda["foto_cliente"],
                                     foto_produto=venda["foto_produto"], data=venda["data"],
                                     preco=venda["preco"], quantidade=venda["quantidade"], unidade=venda["unidade"])
                lista_vendas.add_widget(banner)
        except Exception as excecao:
            print(f"exceção (carregar_todas_vendas) = {excecao}")  # printa a mensagem de erro se existir erro dentro do try

        # preencher o total de vendas
        total_vendas = dicionario_informacoes_vendedor["total_vendas"]
        pagina_vendasoutrovendedor.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

        # preencher foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]  # sempre que eu quiser pegar o id de um cara no main.kv, vou utilizar o self.root.ids passando o id entre colchetes
        avatar = dicionario_informacoes_vendedor["avatar"]  # 'avatar' recebe a foto do vendedor do dicionario_informacoes_vendedor
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # direciona para página vendasoutrovendedorpage
        self.mudar_tela("vendasoutrovendedorpage")


MainApp().run()  # para executar nosso código (aplicativo)

# Comunicação com a api do banco de dados
# comando GET você pega informações do banco
# comando POST você envia informações para o banco, cria informações
# comando PATCH atualiza informações no banco de dados
