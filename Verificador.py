import requests
import bs4
from os import path


#Para que o codigo funcione corretamente no arquivo link os links deve ser
#armazenado da seguinte forma cada link deve estar embaixo do outro!

#http://www.owriezc726nuc3fv.onion/
#http://www.owriezc726nuc3fv.onion/

#site - http://www.owriezc726nuc3fv.onion/ <-- Assim não funciona
#http://www.owriezc726nuc3fv.onion/ - site <-- assim funciona!




def main():
    print('(1)Selecionar arquivo C/Links (2)Verificar Links On')
    try:
        select = int(input('Escolha uma opção: '))
        if select == 1:
            separaLink()
        else:
            if select == 2:
                verificador()
    except:
        print('Digite apenas números!')
        main()


def separaLink():
    # Codigo para abrir arquivos em susa pastas!

    #print('Informe o caminho do arquivo Ex:(c:\user\documentos\links.txt')
    caminho = input('Caminho: ')
    print('Criando arquivo com links para verificação aguarde! ...')
    if path.isfile(caminho):

        lnk = []

        res = open(caminho, encoding='utf8')

        for i in range(99):
            a = res.readline()
            b = a.split('/')
            c = 'http://' + b[2] + '\n'
            lnk.append(c)
        res.close()

        doc2 = open('links-separados.txt', 'a')

        a = len(lnk)
        for i in range(99):
            doc2.write(lnk[i])

        print('Arquivo criado com sucesso!')


        doc2.close()
        main()

    else:
        print('Arquivo não existe')
        separaLink()





def verificador():

    doc = open('links-separados.txt', 'r')
    """
    sites = []
    for j in doc:
        sites.append(j)
    """
    print('Verificando...')

    doc2 = open('sitesOn.txt', 'a')

    for i in doc:
        a = doc.readline()
        z = a.rstrip()
        link = z+'.link'
        r = requests.get(link)
        G = r.status_code
        if G == 200:
            T = requests.get(link)
            tmp = bs4.BeautifulSoup(T.content)
            ti = tmp.title
            nome = str(link) + str(ti) + '\n'
            doc2.write(nome)

            print('Link: ', a.rstrip(), ' - ', ti)

    doc.close()
    doc2.close()
        
main()
"""
#Serve para retirar o \n
.rstrip()
"""
