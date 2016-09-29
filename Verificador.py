import requests
import bs4
import os
from os import path


#Para que o codigo funcione corretamente no arquivo link os links deve ser
#armazenado da seguinte forma cada link deve estar embaixo do outro!

#http://www.owriezc726nuc3fv.onion/
#http://www.owriezc726nuc3fv.onion/

#site - http://www.owriezc726nuc3fv.onion/ <-- Assim não funciona
#http://www.owriezc726nuc3fv.onion/ - site <-- assim funciona!


lista2 = ['']
contador = 0

def main():
    global lista, contador
    #Cria os arquivos caso não exista!
    doc2 = open('sitesOn.txt', 'a')
    doc2.close()

    # Codigo para abrir arquivos em susa pastas!
    print('Informe o nome do arquivo Ex: links.txt')
    local = input('Nome do arquivo: ')
    caminho = os.getcwd() + '\\' + local
    print(caminho)
    #Verifica se o arquivo existe no caminho especificado!
    if path.isfile(caminho):
        print('Criando arquivo com links para verificação aguarde! ...', 3 * '\n')

        lista = ['']


        with open('sitesOn.txt', 'r') as arquivo:

            for l in arquivo:
                primeiro = arquivo.readline()
                segundo = primeiro.split('.onion')
                lista2.append(segundo[0])

        with open(caminho, 'r', encoding='utf8') as res:

            for j in res:
                a = res.readline()
                lista.append(str(a))


        for i in range(1, len(lista)+1):
            a = lista[i]
            b = a.split('/')
            c = 'http://' + b[2]
            d = c.split('.onion')
            duplica(d[0])


        print('Forão adicionados mais %i novos link ao arquivo sitesOn.txt!'%contador)

        print('Deseja verificar mais links?', 3 * '\n')



        try:
            opcao = str(input('(S)Sim - (N)Não: ')).lower()

            if opcao == 's':
                main()

            elif opcao == 'n':
                exit()
        except:
            print('Digite apenas S ou N!')


        res.close()
        main()

    else:
        print('Arquivo não existe')
        main()

#Verifica se o link ja existe no arquivo!
def duplica(link):
    global lista2

    if link in lista2:
        return print('%s.onion - Existente!'%link)

    else:
        return verificador(link+'.onion')


#Serve pra guardar os arquivos novos no arquivo!
def verificador(endereco):
    global contador

    a = endereco
    z = a.rstrip()
    link = z + '.link'
    r = requests.get(link)
    G = r.status_code

    if G == 200:
        contador += 1
        T = requests.get(link)
        tmp = bs4.BeautifulSoup(T.content)
        ti = tmp.title
        nome = str(link) + ' - '
        grava = endereco + str(ti) + '\n'

        doc2 = open('sitesOn.txt', 'a')
        doc2.write(grava)
        doc2.close()
        print('Link: ', a.rstrip(), ' - ', ti)


main()

