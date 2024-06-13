from botoes import ImageButton, LabelButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import requests  # para fazermos a requisição no banco de dados
from kivy.app import App  # importa a classe App
from functools import partial  # para uma função que está sendo passada no on_release, receber uma informação como parâmetro, ela necessita do partial


class BannerVendedor(FloatLayout):  # a classe BannerVendedor será uma subclasse do FloatLayout
    # função __init__ que inicializa o objeto
    def __init__(self, **kwargs):  # keyword arguments, **kwargs para receber um dicionário com todas as colunas com informações da vendas como chave e valor
        super().__init__()  # chamando o __init__ da super classe FloatLayout, trazendo as características do FloatLayout

        with self.canvas:
            self.opacity = 0.8
            Color(rgb=(48/255, 88/255, 99/255, 1))  # HEX #305863
            # Color(rgb=(24/255, 46/255, 45/255, 1))
            # Color(rgb=(0, 0, 0, 1))  # definindo o fundo preto para cada banner
            self.rec = Rectangle(size=self.size, pos=self.pos)  # tamanho e posição do fundo
        self.bind(pos=self.atualizar_rectangle, size=self.atualizar_rectangle)  # para atualizar sempre que rodar a função BannerVendedor

        # passando a informação para única variável
        id_vendedor_valor = kwargs["id_vendedor"]

        # requisição no banco de dados
        link = f'https://aplicativocelularkivy-fefbf-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_valor}"'
        requisicao = requests.get(link)
        requisicao_dicionario = requisicao.json()
        print(f"requisicao_dicionario (BannerVendedor) = {requisicao_dicionario}")

        # pegando o valor do dicionário sem passar a chave para ele
        valor = list(requisicao_dicionario.values())[0]  # valor recebe um dicionário com todas as informações do vendedor
        print(f"valor (BannerVendedor)= {valor}")
        avatar = valor["avatar"]
        total_vendas = valor["total_vendas"]

        # definindo nosso aplicativo para implementar o on_release nos botões
        meu_aplicativo = App.get_running_app()

        imagem = ImageButton(source=f"icones/fotos_perfil/{avatar}",
                             pos_hint={"right": 0.4, "top": 0.9}, size_hint=(0.3, 0.8),
                             on_release=partial(meu_aplicativo.carregar_vendas_vendedor, valor))  # o partial permite passar o 'valor' como parâmetro para função 'carregar_vendas_vendedor'
        label_id = LabelButton(text=f"ID Vendedor: {id_vendedor_valor}",
                               pos_hint={"right": 0.9, "top": 0.9}, size_hint=(0.5, 0.5),
                               on_release=partial(meu_aplicativo.carregar_vendas_vendedor, valor))  # o partial permite passar o 'valor' como parâmetro para função 'carregar_vendas_vendedor'
        label_total = LabelButton(text=f"Total de Vendas: R${total_vendas}",
                                  pos_hint={"right": 0.9, "top": 0.6}, size_hint=(0.5, 0.5),
                                  on_release=partial(meu_aplicativo.carregar_vendas_vendedor, valor))  # o partial permite passar o 'valor' como parâmetro para função 'carregar_vendas_vendedor'

        self.add_widget(imagem)
        self.add_widget(label_id)
        self.add_widget(label_total)

    def atualizar_rectangle(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size
