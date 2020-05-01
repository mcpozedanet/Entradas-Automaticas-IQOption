#coding: iso-8859-15
from iqoptionapi.stable_api import IQ_Option
import logging
import time, configparser
from datetime import datetime

logging.disable(level=(logging.DEBUG))

def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')

    return {'email': arquivo.get('GERAL', 'email'), 'senha': arquivo.get('GERAL', 'senha')}

# VERIFICANDO SE LOGIN ESTÁ CORRETO
    conf = configuracao()
    API = IQ_Option(conf['email'], conf['senha'])
    API.connect()
    
    API.change_balance('PRACTICE') # PRACTICE / REAL


# CARREGA OS SINAIS
def carregar_sinais():  # CARREGA OS SINAIS DA LISTA
    arquivo = open('sinais.txt', encoding='UTF-8')  # -> ABRE O ARQUIVO SINAIS.TXT
    lista = arquivo.read()  # -> LE OS ARQUIVOS DO TXT E ARMAZENA NA VARIAVEL LISTA
    arquivo.close  # -> FECHA A ABERTURA DA LISTA

    lista = lista.split('\n')  # -> SEPARA A LISTA COM QUEBRA DE LINHA

    for index, a in enumerate(lista):  # -> CONTA A QUANTIDADE DE NUMERAÇÃO DE LINHAS DA LISTA
        if a == '':  # -> CONDIÇÃO SE HOUVER ALGUMA LINHA COM ESPAÇO EM BRANCO
            del lista[index]  # -> FUNÇÃO QUE DELETA A LINHA

    return lista  # -> RETORNA A LISTA


lista = carregar_sinais()  # -> ARMAZENA TODA A FUNÇÃO CARREGAR_SINAIS DENTRO DA VARIAVEL LISTA


def timestamp_converter(x):  # FUNÇÃO QUE CONVERTE TIMESTAMP
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora)[:-6]
    # --------------------------------------------------------------------------------------


entrou = 0  # -> INFORMA QUE NÃO HOUVE ENTRADAS NO MOMENTO DENTRO DO LOOP ABAIXO
# Checagem de conexão

while True:
    if API.check_connect() == False:
        print('Erro ao se conectar')

        API.connect()
    else:
        print('\n\nConectado com sucesso')
        break

    time.sleep(1)

# A LISTA ESTÁ EM FORMATO: DATA: 00/00/0000,00:00:00,EURUSD,5,DIREÇÃO,0.00

for sinal in lista:  # ARMAZENA OS DADOS DA LISTA NA VARIAVEL
    dados = sinal.split(',')
    data = dados[0]  # -> ARMAZENA DATA
    hora = dados[1]  # -> ARMAZENA HORA
    par = str(dados[2])  # -> ARMAZENA O PAR
    timeframe = int(dados[3])  # -> ARMAZENA O TIMEFRAME
    direcao = dados[4]  # -> ARMAZENA A DIREÇÃO (CALL OU PUT)
    stake = float(dados[5])  # -> ARMAZENA O VALOR DA ENTRADA
    agora = datetime.now()  # -> ARMAZENA A DATA E HORA ATUAL DO SERVIDOR (ANO/MES/DIA HORA:MINUTO:SEGUNDOS
    data_atual = agora.strftime('%d/%m/%Y')  # -> ARMAZENA A DATA ATUAL PELO FORMATO DIA/MES/ANO DA VARIAVEL AGORA
    while data >= data_atual:  # CONDIÇÃO: ENQUANTO DA DATA FOR MAIOR OU IGUAL A DATA ATUAL EXECUTA OS COMANDOS ABAIXO
        entrou = 1  # -> ARMAZENA 1 CASO TENHA ENTRADO NA CONDIÇÃO ACIMA
        now = datetime.now()  # -> ARMAZENA A DATA ATUAL DO COMPUTADOR NA VARIAVEL NOW
        hora_atual = now.strftime("%H:%M:%S")  # -> SEPARA SOMENTE A HORA DA VARIAVEL NOW
        direction = direcao.lower()  # -> PEGA A DIREÇÃO E DEIXA EM MINÚSCULO PARA NÃO CAUSAR ERRO NAS ENTRADAS
        if hora_atual == dados[1]:  # -> CONDIÇÃO: SE A HORA ATUAL FOR IGUAL A HORA DA LISTA DE SINAIS EXECUTAR OS COMANDOS ABAIXO:
            print('Operação realizada no par: ' + str(par) + ' ás ' + str(hora) + '. Timeframe: ' + str(timeframe) + ', Direção: ' + str(direcao) + ' Stake: ' + str(stake))  # -> MOSTRA OS DADOS DA OPERAÇÃO QUE IRÁ SER REALIZADA
            # status, id = API.buy(int(configs['entrada']), configs['par'], dados[2], int(configs['timeframe']))
            print('=+=+=+' * 20)
            _, id = (API.buy(stake, par, direcao, timeframe))  # -> EXECUTA A OPERAÇÃO
            break
        if entrou == 0:  # -> CONDIÇÃO: SE NÃO ENTROU NO LOOP ENQUANTO DATA FOR MAIOR OU IGUAL A DATA ATUAL INFORMA O ERRO ABAIXO:
            print('Não foi possível executar a operação!')
