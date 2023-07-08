import socket
import threading

# Função para processar as requisições dos clientes
def processar_requisicao(connection, client_address):
    try:
        print("Conexão estabelecida:", client_address)

        while True:
            data = connection.recv(1024).decode('utf-8')
            if data:
                # Processar a requisição recebida
                linha, coluna = data.split()
                linha = int(linha)
                coluna = int(coluna)
                response = processar_requisicao(linha, coluna)

                # Enviar a resposta ao cliente
                connection.send(response.encode('utf-8'))
            else:
                break

    finally:
        # Fechar a conexão
        connection.close()

# Criação do socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vinculação do socket a um endereço e porta
server_address = ('127.0.0.1', 12345)  # exemplo de endereço e porta do servidor
sock.bind(server_address)

# Aguardar por conexões
sock.listen(5)

def start_server():
    while True:
        print("Aguardando por conexões...")
        connection, client_address = sock.accept()

        # Iniciar uma nova thread para lidar com o cliente conectado
        thread = threading.Thread(target=processar_requisicao, args=(connection, client_address))
        thread.start()

start_server()
 
    
