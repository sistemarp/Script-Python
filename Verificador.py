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
        elif select == 2:
            verificador()
        else:
            print('Selecione 1 OU 2!', 3 * '\n')
            main()
    except:
        print('Digite apenas números!', 3*'\n')
        main()


def separaLink():
    # Codigo para abrir arquivos em susa pastas!

    print('Informe o caminho do arquivo Ex:(C:/usuario/documentos/links.txt)')
    caminho = input('Caminho: ')
    print('Criando arquivo com links para verificação aguarde! ...', 3*'\n')

    if path.isfile(caminho):

        rrr = open
        res = open(caminho, 'r', encoding='utf8')
        doc2 = open('links-separados.txt', 'a', encoding='utf8')

        for i in res:
            a = res.readline()
            b = a.split('/')
            c = 'http://' + b[2] + '\n'
            doc2.write(c)


        print('Arquivo criado com sucesso!')

        res.close()
        doc2.close()
        main()

    else:
        print('Arquivo não existe')
        separaLink()





def verificador():

    with open('links-separados.txt', 'r') as doc:

        print('Verificando...')

        for i in doc:
            doc2 = open('sitesOn.txt', 'r')
            a = doc.readline()
            z = a.rstrip()
            link = z + '.link'
            r = requests.get(link)
            G = r.status_code

            if G == 200:
                if z in doc2:
                    print(a, 'Já Existe!')

                else:
                    T = requests.get(link)
                    tmp = bs4.BeautifulSoup(T.content)
                    ti = tmp.title
                    nome = str(link) + str(ti) + '\n'
                    doc2 = open('sitesOn.txt', 'a')
                    doc2.write(nome)
                    doc2.close()
                    print('Link: ', a.rstrip(), ' - ', ti)

        doc.close()
        doc2.close()
        
main()
