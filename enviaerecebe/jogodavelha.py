import socket
import json

# Configurações do servidor
HOST = 'localhost'  # Pode ser o IP do seu servidor
PORT = 12345  # Porta do servidor

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o socket ao endereço e porta definidos
server_socket.bind((HOST, PORT))

# Coloca o socket em modo de escuta
server_socket.listen(1)

print('Aguardando conexões...')

# Aceita uma nova conexão do cliente
client_socket, client_address = server_socket.accept()

print('Cliente conectado:', client_address)

while True:
    # Recebe os dados do cliente
    data = client_socket.recv(1024)

    if not data:
        # O cliente desconectou
        print('Cliente desconectado.')
        break

    # Decodifica a mensagem recebida
    message = data.decode('utf-8')

    # Processa a mensagem recebida do cliente
    # O objeto JSON é passado com dois campos int, linha e coluna, descontruindo abaixo é possível aplicar cada um dos campos às variáveis linha e coluna
    try:
        move = json.loads(message)
        linha = move['linha']
        coluna = move['coluna']

        print('Jogada recebida:', linha, coluna)

        # Aplica a jogada no jogo da velha
        # ...
    except json.JSONDecodeError:
        print('Erro ao decodificar a mensagem JSON.')
    except KeyError:
        print('Chaves "linha" e "coluna" não encontradas na mensagem.')
