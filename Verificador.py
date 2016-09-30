import requests, bs4, os, re
from os import path


#Para que o codigo funcione corretamente no arquivo link os links deve ser
#armazenado da seguinte forma cada link deve estar embaixo do outro!

#http://www.owriezc726nuc3fv.onion/
#http://www.owriezc726nuc3fv.onion/

#site - http://www.owriezc726nuc3fv.onion/ <-- Assim não funciona
#http://www.owriezc726nuc3fv.onion/ - site <-- assim funciona!


lista2 = ['0']
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


        arquivo = open('sitesOn.txt', 'r', encoding='utf8', errors='ignore').readline()

        for l in arquivo:
            segundo = arquivo.split(' ')
            lista2.append(segundo[0])


        res = open(caminho, 'r', encoding='utf8').readlines()


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
    global lista2

    if link in lista2:
        return print('%s.onion - Existente!'%link)

    else:
        return verificador(link)

#Serve pra guardar os arquivos novos no arquivo!
def verificador(endereco):
    global contador

    a = endereco.rstrip()
    link = a + '.link'
    r = requests.get(link)
    G = r.status_code

    if G == 200:
        T = requests.get(link)
        tmp = bs4.BeautifulSoup(T.content)
        ti = tmp.title
        nome = link + ' - '
        grava = nome + str(ti) + '\n'

        contador += 1

        doc2 = open('sitesOn.txt', 'a', encoding='utf8')
        doc2.write(grava)
        doc2.close()
        print('Link: ', link.rstrip(), ' - ', ti)


main()

