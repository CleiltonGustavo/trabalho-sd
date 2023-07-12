import socket
import json

# Configurações do cliente
HOST = 'localhost'  # Pode ser o IP do seu servidor
PORT = 4000  # Porta do servidor

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client_socket.connect((HOST, PORT))

flag = client_socket.recv(1024)
flag = flag.decode('utf-8')
print(flag)
if flag == '1'or 1:
    sua_vez = True
else:
    sua_vez = False    
while True:
    if sua_vez:
        req = client_socket.recv(1024)

        if not req:
            # O servidor desconectou
            print('Servidor desconectado.')
            break

        # Decodifica a mensagem recebida
        mensagem = req.decode('utf-8')

        # Exibe a mensagem de solicitação do servidor
        print(mensagem)

        while True:
            # Prepara os dados da jogada
            linha = input('Digite a linha: ')
            coluna = input('Digite a coluna: ')

            if linha.isdigit() and coluna.isdigit():
                linha = int(linha)
                coluna = int(coluna)

                if linha in [0, 1, 2] and coluna in [0, 1, 2]:
                    break
            print('Valores inválidos! A linha e a coluna devem ser 0, 1 ou 2.')

        jogada = {'linha': linha, 'coluna': coluna}

        # Converte a jogada em JSON
        message = json.dumps(jogada)

        # Envia a mensagem para o servidor
        client_socket.sendall(message.encode('utf-8'))
        sua_vez = False
    else:
        sua_vez = True

    data = client_socket.recv(1024)
    
    #Decodifica mensagem recebida matriz
    matrix = data.decode('utf-8')
    print(matrix)

# Fecha o socket do cliente
client_socket.close()
