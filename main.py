from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window
from kivy.clock import Clock

import random


class Gerenciador(ScreenManager):
	pass

class Game(Screen):
	player = ObjectProperty()
	obstaculos = []

	def __init__(self, **kw):
		super(Game, self).__init__(**kw)
		Clock.schedule_once(self.adiciona_player, .1)
		Clock.schedule_interval(self.adiciona_obstaculo, 1)
		#Clock.schedule_interval(self.adiciona_player, 1)

	def on_touch_down(self, *args, **kwargs):
		print(args, kwargs)
		print(self.player.children, len(self.player.children))

	def adiciona_player(self, *args):
		self.player = Player()
		self.add_widget(self.player)

	def on_pre_enter(self, *args):
		Window.bind(on_keyboard=self.atalhos_teclado, on_key_down=self.key_down, on_key_up=self.key_up)
	
	def key_down(self, win, key, *args):
		if key == 274:
			self.player.estado_normal = False

		elif key == 273:
			self.player.pula = True
			
	def key_up(self, win, key, *args):
		if key == 274:
			self.player.estado_normal = True
		elif key == 273:
			self.player.pula = False

	def atalhos_teclado(self, win, key, *args):
		pass
	
	def adiciona_obstaculo(self, *args):
		obs = Obstaculo()
		self.obstaculos.append(obs)
		self.add_widget(obs, 1)


class Obstaculo(Image):
	allow_stretch = BooleanProperty(True)
	size_hint = None, None
	tipos = ["cacto", "helicoptero"]
	velocidade = Window.width / 2
	aceleracao = 3
	_n = 0

	def __init__(self, **kw):
		super(Obstaculo, self).__init__(**kw)
		self.tipo = random.choice(self.tipos)
		k = random.uniform(.2, .26) if self.tipo == "cacto" else random.uniform(.6, .65)
		if self.tipo == "cacto":
			n = ""
			self.size = 64, 128
		else:
			n = "0"
			self.size = 64, 64
		self.source = self.tipo + n + ".png"
		
		self.texture.mag_filter = "nearest"
		self.pos = Window.width, Window.height * k


		Clock.schedule_interval(self.atualiza, 1/60)
		if self.tipo == "helicoptero":
			Clock.schedule_interval(self.atualiza_helicoptero, 1/60)

	
	def atualiza(self, tempo = 1/60, *args):
		if self.x <= 0:
			return 
		self.velocidade += self.aceleracao * tempo
		self.x -= self.velocidade * tempo

	def atualiza_helicoptero(self, *args):	
		self._n += 1
		self._n = self._n % 3
		self.source = self.tipo + str(self._n) + ".png"
		self.texture.mag_filter = "nearest"


class Player(FloatLayout):
	speed = NumericProperty(300)
	aceleracao = NumericProperty(1000)
	pula = False
	estado_normal = True
	_n = 0
	cima = StringProperty("alto_normal.png")
	baixo = StringProperty("baixo_normal.png")
	_mostrar_partes = False

	#pernas = ObjectProperty()

	def __init__(self, **kw):
		super(Player, self).__init__(**kw)
		self.x = Window.width * .1 
		self.y = Window.height * .3
		Clock.schedule_once(self._carrega_texturas, .1)
		
	def _carrega_texturas(self, tempo=1/20):
		self.ids.cima.texture.mag_filter = "nearest" 
		self.ids.baixo.texture.mag_filter = "nearest"
		Clock.schedule_interval(self.atualiza, 1/60)
		Clock.schedule_interval(self.simula_corrida, 1/60)

		self._partes = {self.ids[key] for key in self.ids.keys() if key not in ["cima", "baixo"]}
	
	def atualiza(self, tempo=1/60, *args):
		#print("pos = ", self.ids.pernas.pos, "\tzise = ", self.ids.pernas.size)
		if not self.esta_no_chao() or self.speed > 0:
			self.speed += -self.aceleracao * tempo
			self.y += self.speed * tempo
		if self.pula and self.esta_no_chao():
			self.speed = 600

		self._muda_estado_cima()

	def _muda_estado_cima(self):
		if self.estado_normal:
			self.cima = "alto_normal.png"
			cabeca = self.ids.cabeca
			cabeca.pos = self.x + self.width * 0, self.y + self.height * 0

			self.ids.maos.pos = (
				self.x + self.width * 0, self.y + self.height * 0
			)


		else:
			self.cima = "alto_abaixado.png"
			self.ids.cima.texture.mag_filter = "nearest"
			cabeca = self.ids.cabeca
			cabeca.pos = self.x + self.width * 0.16, self.y + self.height * -0.16

			self.ids.maos.pos = (
				self.x + self.width * 0.065, self.y + self.height * -0.12
			)
		
		self.ids.cima.texture.mag_filter = "nearest"
		
	
	def simula_corrida(self, *args):
		if self.esta_no_chao():
			self._n += 1
			self._n = self._n % 2
			self.baixo = "baixo_" + str(self._n) + ".png"
			self.ids.baixo.texture.mag_filter = "nearest"


	def esta_no_chao(self):
		if self.y <= Window.height * .3:
			return True
		else:
			return False
		


class Dino(App):
	def build(self):
		return Gerenciador()
	
	

Dino().run()
