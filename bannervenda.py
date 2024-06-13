from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

# atenção: elementos estáticos podem ser criados diretamente no arquivo .kv, mas elementos dinâmicos precisam ser criados no arquivo em python
# terceira etapa para criação do banner, criar essa classe BannerVenda determinando como cada elemento será criado
# criando o widget personalizado


class BannerVenda(GridLayout):  # a classe BannerVenda será uma subclasse do GridLayout
    # função __init__ que inicializa o objeto
    def __init__(self, **kwargs):  # keyword arguments, **kwargs para receber um dicionário com todas as colunas com informações da vendas como chave e valor
        # kwargs = {"cliente": "mundial", "foto_cliente": "mundial.png"...}
        self.rows = 1  # sempre o GridLayout precisa ter o número de linhas ou de colunas
        super().__init__()  # chamando o __init__ da super classe GridLayout, trazendo as características do GridLayout

        with self.canvas:
            self.opacity = 0.8
            Color(rgb=(48/255, 88/255, 99/255, 1))  # HEX #305863
            # Color(rgb=(24/255, 46/255, 45/255, 1))
            # Color(rgb=(0, 0, 0, 1))  # definindo o fundo preto para cada banner
            self.rec = Rectangle(size=self.size, pos=self.pos)  # tamanho e posição do fundo
        self.bind(pos=self.atualizar_rectangle, size=self.atualizar_rectangle)  # para atualizar sempre que rodar a função BannerVenda
        # kwargs = {"cliente": "mundial", "foto_cliente": "mundial.png"}

        # passando a informação para cada variável
        cliente = kwargs["cliente"]
        foto_cliente = kwargs["foto_cliente"]
        produto = kwargs["produto"]
        foto_produto = kwargs["foto_produto"]
        data = kwargs["data"]
        unidade = kwargs["unidade"]
        quantidade = float(kwargs["quantidade"])
        preco = float(kwargs["preco"])

        #ESQUERDA
        esquerda = FloatLayout()
        esquerda_imagem = Image(
            pos_hint={"right": 1, "top": 0.95},  # posição
            size_hint=(1, 0.75),  # tamanho
            source=f"icones/fotos_clientes/{foto_cliente}"  # fonte da foto
        )
        esquerda_label = Label(
            text=cliente,
            pos_hint={"right": 1, "top": 0.2},
            size_hint=(1, 0.2)
        )
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        #MEIO
        meio = FloatLayout()
        meio_imagem = Image(
            pos_hint={"right": 1, "top": 0.95},
            size_hint=(1, 0.75),
            source=f"icones/fotos_produtos/{foto_produto}"
        )
        meio_label = Label(
            text=produto,
            pos_hint={"right": 1, "top": 0.2},
            size_hint=(1, 0.2)
        )
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        #DIREITA
        direita = FloatLayout()
        direita_label_data = Label(
            text=f"Data: {data}",
            pos_hint={"right": 1, "top": 0.9},
            size_hint=(1, 0.33)
        )
        direita_label_preco = Label(
            text=f"Preço: R${preco:,.2f}",
            pos_hint={"right": 1, "top": 0.65},
            size_hint=(1, 0.33)
        )
        direita_label_quantidade = Label(
            text=f"{quantidade} {unidade}",
            pos_hint={"right": 1, "top": 0.4},
            size_hint=(1, 0.33)
        )
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_quantidade)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rectangle(self, *args):  # recebe vários argumentos como parâmetros
        self.rec.pos = self.pos
        self.rec.size = self.size

