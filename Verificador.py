import requests, bs4, os, re
from os import path

#Programa que verifica link On na rede onion por meio de 3 nós diferentes!
#Created By: THX

lista1 = []
lista2 = []
contador = 0

def main():
    global lista, contador

    # Codigo para abrir arquivos em susa pastas!
    print('Informe o nome do arquivo Ex: links.txt')
    local = input('Nome do arquivo de links .onion: ')
    caminho = os.getcwd() + '\\' + local + '.txt'

    #Cria arquivo sitesOn.txt caso nao exista no local!
    if not path.isfile(caminho+'/sitesOn.txt'):
        doc2 = open('sitesOn.txt', 'a')
    #Verifica se o arquivo existe no caminho especificado!
    if path.isfile(caminho):
        print('Criando arquivo com links para verificação aguarde! ...', 3 * '\n')

        lista = ['0']

        with open('sitesOn.txt', 'r', encoding='utf8', errors='ignore')as arquivo:
            for y in arquivo:
                primeiro = arquivo.readline()
                segundo = primeiro.split(' ')
                terceriro = segundo[0].rstrip()
                lista1.append(terceriro)

        for endereco in lista1:
            match = re.search('(http?\:\/\/.*?\.onion)', endereco.replace(' ', ''))
            if match:
                cr = match.groups()[0].rstrip()
                lista2.append(cr)


        res = open(caminho, 'r', encoding='utf8', errors='ignore').readlines()


        #Neste forloop serve para pegar apenas o meio do link e reescrever sem espaços
        for link in res:
            match = re.search('(http?\:\/\/.*?\.onion)', link.replace(' ', ''))
            if match:
                cl = match.groups()[0].rstrip()
                duplica(cl)#Envia para verificar se ta On e se ja existe no arquivo linksOn.txt

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
    global lista1

    if link in lista1:
        print('%s - Existente!'%link)

    else:
        verificador(link)

#Serve pra guardar os arquivos novos no arquivo!
def verificador(endereco):

    try:
        a = endereco.rstrip()
        link = a + '.link'
        r = requests.get(link)
        G = r.status_code

        if G == 200:
            gravaLink(a, '.link')
        else:
            try:
                a = endereco.rstrip()
                link = a + '.to'
                r = requests.get(link)
                G = r.status_code

                if G == 200:
                    gravaLink(a, '.to')
                else:
                    try:
                        a = endereco.rstrip()
                        link = a + '.city'
                        r = requests.get(link)
                        G = r.status_code

                        if G == 200:
                            gravaLink(a, '.city')
                    except:
                        pass
            except:
                pass
    except:
        pass


def gravaLink(valor, modo):
    global contador

    ver = valor + modo
    T = requests.get(ver)
    tmp = bs4.BeautifulSoup(T.content, "html.parser")
    ti = tmp.title
    nome = valor + ' - '
    grava = nome + str(ti) + '\n'

    contador += 1

    doc2 = open('sitesOn.txt', 'a', encoding='utf8', errors='ignore')
    doc2.write(grava)
    doc2.close()
    print('Link: ', valor.rstrip(),modo , ' - ', ti)

main()
