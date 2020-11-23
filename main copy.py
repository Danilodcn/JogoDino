from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.clock import Clock


class Gerenciador(ScreenManager):
	pass

class Game(Screen):
	def __init__(self, **kw):
		super(Game, self).__init__(**kw)
		Clock.schedule_once(self.criar_play, 1)
	
	def criar_play(self, *args):
		self.player = Player()
		self.add_widget(self.player)
		Window.bind(on_keyboard=self.atalhos_teclado, on_key_down=self.key_down, on_key_up=self.key_up)

	def on_pre_enter(self, *args):
		pass

	def key_up(self, a, key, *args):
		if key == 273:
			self.player.pula = False

	def key_down(self, a, key, *args):
		if key == 273:
			self.player.pula = True

	def atalhos_teclado(self, win, key, *args):
		if key == 273:
			pass
		


class Player(BoxLayout):
	speed = NumericProperty(300)
	aceleracao = NumericProperty(1000)
	pula = False
	__n = 0
	cima = StringProperty("")
	baixo = StringProperty("")

	def __init__(self, **kw):
		super(Player, self).__init__(**kw)
		self.x = Window.width * .1 
		self.y = Window.height * .2987
		Clock.schedule_interval(self.update, 1/60)
		Clock.schedule_interval(self.troca_texture, 1 / 20)

	def troca_texture(self, *args):
		if self.esta_no_chao():
			self.__n += 1
			self.__n = self.__n % 2
			if self.__n == 0:
				self.source = "player0.png"
			else:
				self.source = "player1.png"
		elif not self.esta_no_chao():
			self.source = "player.png"




	def update(self, tempo=1/60, pula=False):
		if not self.esta_no_chao() or self.speed > 0:
			self.speed += -self.aceleracao * tempo
			self.y += self.speed * tempo
		
		if self.pula and self.esta_no_chao():
			self.speed = 600

		#print(self.esta_no_chao(), self.pula, self.y, self.speed)

	def esta_no_chao(self):
		if self.y <= Window.height * .3:
			return True
		else:
			return False


class Dino(App):
	def build(self):
		return Gerenciador()

Dino().run()
