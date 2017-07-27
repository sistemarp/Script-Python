import pygame, sys, os, MySQLdb, datetime, random
from pygame.locals import *


class Banco(object):
    def dados(self):
        try:
            conecta = MySQLdb.connect(host='localhost', user='root', passwd='toor', db='mmatriz')
            return conecta
        except Exception as e:
            print('Deu erro no Banco de Dados --> ', str(e))


class Jogo(pygame.sprite.Sprite):
    banco = Banco().dados()

    def main(self):
        scala = (1360, 720)
        pygame.init()
        tela = pygame.display.set_mode(scala, pygame.FULLSCREEN)
        pygame.display.set_caption('Matriz Caca Niquel')
        frame = pygame.time.Clock()

        back_ground = pygame.image.load(os.getcwd() + os.sep + '_imagens' + os.sep + 'fundo.jpg')
        sobre_fundo = pygame.image.load(os.getcwd() + os.sep + '_imagens' + os.sep + 'sob-fundo.png')

        # Cria um estilo de fonte padrão para ser exibido na tela
        style = pygame.font.get_default_font()
        font = pygame.font.SysFont(style, 65)
        font_pago = pygame.font.SysFont(style, 30)

        credito = 0
        premio = 0
        aposta = 1
        pago = 0
        valor_aposta = 1
        linha = 1

        cor_amarela = (196, 196, 196)
        txt_credito = font.render(str(credito), 1, cor_amarela)
        txt_premio = font.render(str(premio), 1, cor_amarela)
        txt_aposta = font_pago.render(str(aposta), 1, cor_amarela)
        txt_pago = font_pago.render(str(pago), 1, cor_amarela)
        txt_valor_aposta = font.render(str(valor_aposta), 1, cor_amarela)
		
		tela_jogo: True
		tela_config = False
		
		
        while True:
			if tela_jogo:
				for event in pygame.event.get():
					# Captura evento QUIT que fexa o programa no X
					if event.type == pygame.QUIT:
						pygame.quit()  # Fexa o programa ao paertar no X
						sys.exit()  # Finaliza processos ao fexar o programa

					# Captura evento do mouse
					if event.type == pygame.MOUSEBUTTONDOWN:
						print(pygame.mouse.get_pos())
						

					# Capttura eventos do teclado
					if event.type == pygame.KEYDOWN:
						if event.key == K_q:  # Informa qual é o evento
							pygame.quit()
							sys.exit()

						# Eventos de inserir nota
						if event.key == 49:
							credito += 200
							txt_credito = font.render(str(credito), 1, cor_amarela)
							self.salva('credito', str(credito))
						if event.key == 50:
							credito += 500
							txt_credito = font.render(str(credito), 1, cor_amarela)
							self.salva('credito', str(credito))
						if event.key == 51:
							credito += 1000
							txt_credito = font.render(str(credito), 1, cor_amarela)
							self.salva('credito', str(credito))
						if event.key == 52:
							credito += 2000
							txt_credito = font.render(str(credito), 1, cor_amarela)
							self.salva('credito', str(credito))
						if event.key == 53:
							credito += 5000
							txt_credito = font.render(str(credito), 1, cor_amarela)
							self.salva('credito', str(credito))

						# So meche na maquina com credito
						if credito > 0:
							# Evento de inserir aposta
							if event.key == pygame.K_a:
								if aposta <= 10:
									aposta += 1
									txt_aposta = font_pago.render(str(aposta), 1, cor_amarela)
									self.salva('aposta', str(aposta))

							if event.key == pygame.K_s:
								if aposta != 1:
									aposta -= 1
									txt_aposta = font_pago.render(str(aposta), 1, cor_amarela)
									self.salva('aposta', str(aposta))

							if event.key == pygame.K_d:
								valor_aposta += 1
								txt_valor_aposta = font.render(str(valor_aposta), 1, cor_amarela)
								self.salva('valor_aposta', str(aposta))

							if event.key == pygame.K_g:
								print(self.roleta(aposta, linha))
								#print('Aposta= %s, ValorAP= %s, credito=%s, pago=%s' % (aposta, valor_aposta, (credito - aposta), pago))

				# Regula a frequencia de atualização da tela "Frame"
				frame.tick(30)

				# Imprime BackGrounds
				tela.blit(pygame.transform.scale(back_ground, scala), (0, 0))  # Deixa Scalavel
				tela.blit(pygame.transform.scale(sobre_fundo, scala), (0, 0))

				# imprime Textos
				tela.blit(txt_credito, (335, 55))  # Imprime na tela OBS sempre apos os bcg pois imprime sequencial
				tela.blit(txt_aposta, (1024, 115))
				tela.blit(txt_premio, (704, 55))
				tela.blit(txt_pago, (214, 55))
				tela.blit(txt_valor_aposta, (1073, 55))

				# Ativa SCLE de tela
				pygame.display.flip()

				# Serve para atualizar a tela a cada loop
				pygame.display.update()
				
			elif tela_config:
				
				cor_amarela = (196, 196, 196)
				txt_credito = font.render(str('tela de configuração'), 1, cor_amarela)
				
				
				
				# Regula a frequencia de atualização da tela "Frame"
				frame.tick(30)

				# Imprime BackGrounds
				tela.blit(pygame.transform.scale(back_ground, scala), (0, 0))  # Deixa Scalavel
				tela.blit(pygame.transform.scale(sobre_fundo, scala), (0, 0))
				
				pygame.display.flip()
				pygame.display.update()

    def roleta(self, aposta, linhas):
        data = self.banco
        var = "SELECT reten FROM user WHERE usuario = 'admin'"
        ex = data.cursor()
        ex.execute(var)

        #Pega Valor do Banco par informar o valor a reter
        RET = ex.fetchall()[0][0]

        #referencia da imagens da roleta
        imagens = {'01': '01.jpg', '02': '02.jpg', '03': '03.jpg', '04': '04.jpg', '05': '05.jpg', '06': '06.jpg', '07': '07.jpg',
                   '08': '08.jpg', '09': '09.jpg', '10': '10.jpg' }

        #Lista com valores para sorteio quanto mais numero maior a retenção
        retencao = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

        if RET > '1':
            for add in range(int(RET)):
                retencao.append('03')
                retencao.append('04')
                retencao.append('05')
                retencao.append('06')
                retencao.append('07')
                retencao.append('08')
                retencao.append('09')
                retencao.append('10')

        img = []
        for i in range(1, 10):
            img.append(imagens[random.choice(retencao)])
        return img

    def salva(self, tipo, valor):
        data = self.banco
        relogio = str(datetime.datetime.now()).split('.')[0]
        hora = relogio
        # Salva ultimo estado do credito da maquina
        if tipo == 'credito':
            var = "INSERT INTO ultima_aposta (id, B_aposta, B_premio, B_pago, B_credito, B_valor_aposta, data) VALUES (NULL, '', '', '', '%s', '', '%s');" % (
                valor, hora)
            grava = data.cursor()
            grava.execute(var)
            data.commit()

        if tipo == 'aposta':
            var = "INSERT INTO ultima_aposta (id, B_aposta, B_premio, B_pago, B_credito, B_valor_aposta, data) VALUES (NULL, '%s', '', '', '', '', '%s');" % (
                valor, hora)
            grava = data.cursor()
            grava.execute(var)
            data.commit()

        if tipo == 'premio':
            var = "INSERT INTO ultima_aposta (id, B_aposta, B_premio, B_pago, B_credito, B_valor_aposta, data) VALUES (NULL, '', '%s', '', '', '', '%s');" % (
                valor, hora)
            grava = data.cursor()
            grava.execute(var)
            data.commit()

        if tipo == 'pago':
            var = "INSERT INTO ultima_aposta (id, B_aposta, B_premio, B_pago, B_credito, B_valor_aposta, data) VALUES (NULL, '', '', '%s', '', '', '%s');" % (
                valor, hora)
            grava = data.cursor()
            grava.execute(var)
            data.commit()

        if tipo == 'valor_aposta':
            var = "INSERT INTO ultima_aposta (id, B_aposta, B_premio, B_pago, B_credito, B_valor_aposta, data) VALUES (NULL, '', '', '', '', '%s', '%s');" % (
                valor, hora)
            grava = data.cursor()
            grava.execute(var)
            data.commit()


if __name__ == '__main__':
    Jogo().main()
