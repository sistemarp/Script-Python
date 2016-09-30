import requests, bs4, os, re
from os import path


#Para que o codigo funcione corretamente no arquivo link os links deve ser
#armazenado da seguinte forma cada link deve estar embaixo do outro!

#http://www.owriezc726nuc3fv.onion/
#http://www.owriezc726nuc3fv.onion/

#site - http://www.owriezc726nuc3fv.onion/ <-- Assim não funciona
#http://www.owriezc726nuc3fv.onion/ - site <-- assim funciona!


lista1 = []
lista2 = []
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
                lista2.append(match.groups()[0])


        res = open(caminho, 'r', encoding='utf8', errors='ignore').readlines()


        #Neste forloop serve para pegar apenas o meio do link e reescrever sem espaços
        for link in res:
            match = re.search('(http?\:\/\/.*?\.onion)', link.replace(' ', ''))
            if match:
                duplica(match.groups()[0])#Envia para verificar se ta On e se ja existe no arquivo linksOn.txt

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
        return print('%s.onion - Existente!'%link)

    elif not link in lista2:
        return verificador(link)

    else:
        print('ta dando erro ainda!')

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
    print('Link: ', valor.rstrip(), ' - ', ti)

main()

