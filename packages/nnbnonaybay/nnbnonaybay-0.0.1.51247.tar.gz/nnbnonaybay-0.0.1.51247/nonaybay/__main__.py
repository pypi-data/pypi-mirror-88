from __future__ import print_function

from os import system

from pick import pick

from nonaybay.create_directory.index import createdirectory

title = 'Escolha o que fazer: '
options = [
    {'name': 'Criar o diretório de trabalho'},
    {'name': 'Instalar o AndroidSDK e Java'},
]


def getfunction(option):
    return '{0}'.format(option.get('name'))


option, index = pick(options, title, indicator=' ~> ', options_map_func=getfunction)

if index == 0:
    system('clear')
    createdirectory()
    system('clear')
elif index == 1:
    system('clear')
    print('Ainda não consigo fazer isso!')
    system('clear')
