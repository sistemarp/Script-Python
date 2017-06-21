import os, md5, android, time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty

droid = android.Android()

class MainScreen(Screen):
	logado_on_off = False

	def logarConta(self, senha):
		if self.logado_on_off == False:
			path = os.sep+'home'+os.sep+'anderson'+os.sep+'Documentos'+os.sep+'scrypts'+os.sep+'logar.txt'
			if os.path.isfile(path):
				arq = open(path, 'r').readlines()

				if arq != ():
					password = md5.md5(senha).hexdigest()
					if arq[0].rstrip() == password:
						print('Logado!')
						self.logado_on_off = True
						app = App.get_running_app()
						app.root.current = 'logado'

					else:
						print('Usuario ou Senha esta Incorreto!')

			else:
				arq = open(path, 'w')
				pas = md5.md5('admin')
				arq.write(pas.hexdigest())
				arq.close()

class AnotherScreen(Screen):

	phone=''
	reset=''
	apaga=''
	localiza=''

	def configura(self, senha, celular, local, apaga, reseta):
		#arqpath = os.sep+'storage'+os.sep+'config.txt' #Arquivo de no celular
		path = os.sep+'home'+os.sep+'anderson'+os.sep+'Documentos'+os.sep+'scrypts'+os.sep+'logar.txt'
		arqpath = os.sep+'home'+os.sep+'anderson'+os.sep+'Documentos'+os.sep+'scrypts'+os.sep+'config.txt'

		if not os.path.isfile(arqpath) or os.path.isfile(path):
			arq = open(path, 'a')
			arq2 = open(arqpath, 'a')

		arqpass = open(path, 'w')
		cfg = open(arqpath, 'w')

		config='config=1'
		cfg.write(config+'\n')
		cfg.write(celular+'\n')
		cfg.write(reseta+'\n')
		cfg.write(apaga+'\n')
		cfg.write(local)
		arqpass.write(md5.md5(senha).hexdigest())

		arqpass.close()
		cfg.close()
		AnotherScreen.on_pause()
		


	def on_pause(self):
		self.main()


	def main(self):
		global phone, reset, apaga, localiza
		try:
			while True:
				#arqpath = os.sep+'storage'+os.sep+'config.txt' #Arquivo de config no celular
				arqpath = os.sep+'home'+os.sep+'anderson'+os.sep+'Documentos'+os.sep+'scrypts'+os.sep+'config.txt'
				if os.path.isfile(arqpath):
					cfg=open(arqpath, 'r').readlines()
					if len(cfg) >= 4:
						phone = cfg[1].rstrip()
						reset = cfg[2].rstrip()
						apaga = cfg[3].rstrip()
						localiza = cfg[4]
						self.loop()

		except Exception as e:
			print('Ocorreu o seguinte erro: '+ e.message)
		 

	def loop(self):
		global localiza, apaga, reset
		try:
			 #path = os.sep+'storage'+os.sep+'smsid.txt' #Arquivo de config no celular
			path = os.sep+'home'+os.sep+'anderson'+os.sep+'Documentos'+os.sep+'scrypts'+os.sep+'smsid.txt'
			if not os.path.isfile(path):
				arq = open(path, 'a')
				self.main()

			arq = open(path, 'r').read().split('\n')
			while True:
				msg = droid.smsGetMessageIds(False, 'inbox').result
				if msg != []:
					for smsid in msg:
						sm = droid.smsGetMessageById(smsid).result
						if sm['address'][-9::] == phone[-9::]:

							if sm['body'].lower() == localiza.lower():
								if not sm['date'] in arq:
									arq = open(path, 'a')
									arq.write(sm['date']+'\n')
									arq.close()
									return self.gps(smsid)

								elif sm['body'].lower() == apaga.lower():
									if not sm['date'] in arq:
										arq = open(path, 'a')
										arq.write(sm['date']+'\n')
										arq.close()
										return self.delete(smsid)

								elif sm['body'].lower() == reset.lower():
									if not sm['date'] in arq:
										arq = open(path, 'a')
										arq.write(sm['date']+'\n')
										arq.close()
										return self.resetar()
		except Exception as e:
			print('Ocorreu o seguinte erro: '+ e.message);
			self.main()


	def resetar(self):
	    #arqpath = os.sep+'storage'+os.sep+'config.txt' #Arquivo de config no celular
			arqpath = os.sep+'home'+os.sep+'anderson'+os.sep+'Documentos'+os.sep+'scrypts'+os.sep+'config.txt'
			if os.path.isfile(arqpath):
				os.remove(arqpath)
				self.main()
			self.main()

	def gps(self, smid):
		while True:
			droid.toggleWifiState(True)
			local = droid.startLocating()
			time.sleep(10)
			event=droid.readLocation().result
			if event != {}:
				latitude=event['gps']['latitude']
				longitude=event['gps']['longitude']
				return self.send(smid, latitude, longitude)

			elif event != {}:
				latitude=event['network']['latitude']
				longitude=event['network']['longitude']
				return self.send(smid, latitude, longitude)
			
	def send(self, ss, lat, lon):
		global email
		try:
			msg='Aparelho Localizado:Latitude: %s Longitude: %s'%(str(lat), str(lon))
			tel = '9090'+phone[-9::]
			droid.smsSend(phone[-9::], msg)
			droid.smsSend(tel, msg)
			droid.smsDeleteMessage(ss)
			self.main()

		except Exception as e:
			print('Ocorreu o seguinte erro: '+ e.message);
			self.main()


class ScreenManagement(ScreenManager):
	pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
	 def build(self):
	 	return presentation

if __name__ == '__main__':
	MainApp().run()
