import socket
import json
from cryptography.fernet import Fernet

#Configurações do cliente
HOST = 'localhost'  
PORT = 12345  

#Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conecta ao servidor
client_socket.connect((HOST, PORT))

print('Aguardando o adversário...')

flag = client_socket.recv(1024)
flag = flag.decode('utf-8')
#print(flag)
if flag == '1'or 1:
    sua_vez = True
else:
    sua_vez = False    
while True:
    if sua_vez:
        req = client_socket.recv(1024)

        if not req:
            #O servidor desconectou
            print('Servidor desconectado.')
            break

        with open('chave.txt', 'rb') as file:
            chaveCripto = file.read()

        #Faz um objeto fernet a partir da chave de criptografia do servidor
        fernet = Fernet(chaveCripto)

        mensagemDecriptada = fernet.decrypt(req)

        #Decodifica a mensagem decriptada
        mensagemDecodificada = mensagemDecriptada.decode('utf-8')

        #Exibe a mensagem de solicitação do servidor
        print(mensagemDecodificada)

        while True:
            #Prepara os dados da jogada
            linha = input('Digite a linha: ')
            coluna = input('Digite a coluna: ')

            if linha.isdigit() and coluna.isdigit():
                linha = int(linha)
                coluna = int(coluna)

                if linha in [0, 1, 2] and coluna in [0, 1, 2]:
                    break
            print('Valores inválidos! A linha e a coluna devem ser 0, 1 ou 2.')

        jogada = {'linha': linha, 'coluna': coluna}

        #Converte a jogada em JSON
        message = json.dumps(jogada)

        #Criptografa a mensagem
        messageCripto = fernet.encrypt(message.encode('utf-8'))

        #Envia a mensagem criptografada para o servidor
        client_socket.sendall(messageCripto)
        sua_vez = False
    else:
        sua_vez = True

    data = client_socket.recv(1024)

    matrixDecriptada = fernet.decrypt(data)

    matrixDecodificada = matrixDecriptada.decode('utf-8')
    
    print(matrixDecodificada)

#Fecha o socket do cliente
client_socket.close()
