import socket
import json

# Configurações do cliente
HOST = 'localhost'  # Pode ser o IP do seu servidor
PORT = 12345  # Porta do servidor

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client_socket.connect((HOST, PORT))

# Prepara os dados da jogada
linha = 1
coluna = 2
jogada = {'linha': linha, 'coluna': coluna}

# Converte a jogada em JSON
message = json.dumps(jogada)

# Envia a mensagem para o servidor
client_socket.sendall(message.encode('utf-8'))

# Fecha o socket do cliente
client_socket.close()
