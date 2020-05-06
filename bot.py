# coding: iso-8859-15
from iqoptionapi.stable_api import IQ_Option
import logging
import time, configparser
from datetime import datetime

logging.disable(level=(logging.DEBUG))


def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')

    return {'email': arquivo.get('GERAL', 'email'), 'senha': arquivo.get('GERAL', 'senha')}


conf = configuracao()
API = IQ_Option(conf['email'], conf['senha'])
API.connect()

API.change_balance('PRACTICE')


def carregar_sinais():
    arquivo = open('sinais.txt', encoding='UTF-8')
    lista = arquivo.read() 
    arquivo.close

    lista = lista.split('\n')

    for index, a in enumerate(lista):
        if a == '':
            del lista[index]

    return lista


lista = carregar_sinais()


def timestamp_converter(x):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora)[:-6]
    # --------------------------------------------------------------------------------------


entrou = 0


while True:
    if API.check_connect() == False:
        print('Erro ao se conectar')

        API.connect()
    else:
        print('\n\nConectado com sucesso')
        break

    time.sleep(1)

for sinal in lista:
    dados = sinal.split(',')
    data = dados[0]
    hora = dados[1]
    par = str(dados[2])
    timeframe = int(dados[3])
    direcao = dados[4]
    stake = float(dados[5])
    agora = datetime.now()
    data_atual = agora.strftime('%d/%m/%Y')
    while data >= data_atual:
        entrou = 1
        now = datetime.now()
        hora_atual = now.strftime("%H:%M:%S")
        direction = direcao.lower()
        if hora_atual == dados[
            1]:
            print('Operação realizada no par: ' + str(par) + ' ás ' + str(hora) + '. Timeframe: ' + str(
                timeframe) + ', Direção: ' + str(direcao) + ' Stake: ' + str(
                stake))
            print('=+=+=+' * 20)
            _, id = (API.buy(stake, par, direcao, timeframe))
            break
        if entrou == 0:
            print('Não foi possível executar a operação!')
