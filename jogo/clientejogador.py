import socket
import json

# Configurações do cliente
HOST = 'localhost'  # Pode ser o IP do seu servidor
PORT = 12345  # Porta do servidor

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client_socket.connect((HOST, PORT))

while True:
    # Recebe a mensagem de solicitação do servidor
    data = client_socket.recv(1024)

    if not data:
        # O servidor desconectou
        print('Servidor desconectado.')
        break

    # Decodifica a mensagem recebida
    mensagem = data.decode('utf-8')

    # Exibe a mensagem de solicitação do servidor
    print(mensagem)

    # Prepara os dados da jogada
    linha = int(input('Digite a linha: '))
    coluna = int(input('Digite a coluna: '))
    jogada = {'linha': linha, 'coluna': coluna}

    # Converte a jogada em JSON
    message = json.dumps(jogada)

    # Envia a mensagem para o servidor
    client_socket.sendall(message.encode('utf-8'))

# Fecha o socket do cliente
client_socket.close()
