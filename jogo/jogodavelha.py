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
server_socket.listen(2)  # Permite duas conexões simultâneas

print('Aguardando conexões...')

# Aceita as conexões dos dois clientes
clients = []
for _ in range(2):
    client_socket, client_address = server_socket.accept()
    print('Cliente conectado:', client_address)
    clients.append(client_socket)

# Jogo da velha
matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def Linha(i):
    aux = matriz[i][0] + matriz[i][1] + matriz[i][2]
    return aux

def Coluna(i):
    aux = matriz[0][i] + matriz[1][i] + matriz[2][i]
    return aux

def DiagP():
    aux = matriz[0][0] + matriz[1][1] + matriz[2][2]
    return aux

def DiagS():
    aux = matriz[2][0] + matriz[1][1] + matriz[0][2]
    return aux

def Teste():
    x = 0

    for i in range(3):
        l = Linha(i)
        if l == 3 or l == -3:
            st = "linha " + str(i)
            x = l
            return True
        else:
            c = Coluna(i)
            if c == 3 or c == -3:
                st = "coluna " + str(i)
                x = c
                return True

    dp = DiagP()
    if dp == 3 or dp == -3:
        st = "Diagonal principal"
        x = dp
        return True
    else:
        ds = DiagS()
        if ds == 3 or ds == -3:
            st = "Diagonal secundaria"
            x = ds
            return True

    return False


def XO(aux):
    if aux == 0:
        return '.'
    elif aux == -1:
        return 'X'
    elif aux == 1:
        return 'O'


def printm():
    print(XO(matriz[0][0]), " ", XO(matriz[0][1]), " ", XO(matriz[0][2]))
    print(XO(matriz[1][0]), " ", XO(matriz[1][1]), " ", XO(matriz[1][2]))
    print(XO(matriz[2][0]), " ", XO(matriz[2][1]), " ", XO(matriz[2][2]))


turn = 0
fim = False

def solicitar_jogada(client_socket):
    mensagem = 'FAÇA A JOGADA ' + str(turn + 1) + ': '
    client_socket.sendall(mensagem.encode('utf-8'))

while True:
    try:
        while not fim:
            client_socket = clients[turn % 2]
            solicitar_jogada(client_socket)
            
            # Recebe os dados do cliente
            data = client_socket.recv(1024)

            if not data:
                # O cliente desconectou
                print('Cliente desconectado:', client_socket.getpeername())
                break

            # Decodifica a mensagem recebida
            message = data.decode('utf-8')

            jogada = json.loads(message)
            l = jogada['linha']
            c = jogada['coluna']

            if turn == 9:
                print("Velha")
            else:
                print("jogada", turn + 1)
                print('Jogada recebida:', l, c)
                linha = l
                coluna = c
                if matriz[l][c] == 0:
                    matriz[l][c] = pow(-1, turn + 1)
                    printm()
                    if Teste():
                        print("O ganhador é o jogador:", turn + 1)
                        fim = True
                    turn += 1
                else:
                    print("Localização já preenchida")

    except json.JSONDecodeError:
        print('Erro ao decodificar a mensagem JSON.')
    except KeyError:
        print('Chaves "linha" e "coluna" não encontradas na mensagem.')

    # Fecha a conexão com os clientes e o socket do servidor
    for client_socket in clients:
        client_socket.close()
    server_socket.close()
