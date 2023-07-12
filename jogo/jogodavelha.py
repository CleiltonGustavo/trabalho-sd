import socket
import json
from cryptography.fernet import Fernet

#Gerar um chave de criptografia que será utilizada para criptografar e decriptografar as mensagens enviadas pelo servidor e pelo cliente.
chaveCripto = Fernet.generate_key()

#Guardar a chave de criptografia num txt
with open('chave.txt', 'wb') as file:
    file.write(chaveCripto)

#Objeto criado em cima da chaveCripto
fernet = Fernet(chaveCripto)

#Host (que pode ser o ip do server) e Porta a ser utilizada pelo socket
HOST = 'localhost'
PORT = 12345  

#Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Liga o socket ao endereço e porta especificados
server_socket.bind((HOST, PORT))

#Permite o socket escutar até dois clientes
server_socket.listen(2) 

print('Aguardando conexões...')

#Aceita as conexões dos dois clientes
clients = []
for _ in range(2):
    client_socket, client_address = server_socket.accept()
    print('Cliente conectado:', client_address)
    clients.append(client_socket)

#Serve para determinar quem começa
clients[0].sendall("1".encode('utf-8'))
clients[1].sendall("0".encode('utf-8'))

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
        return '|_*_|'
    elif aux == -1:
        return '|_X_|'
    elif aux == 1:
        return '|_O_|'


def printm(i):

    string = "JOGADA " + str(i + 1) + '\n'
    string = string + XO(matriz[0][0]) + " " + XO(matriz[0][1]) + " " + XO(matriz[0][2]) + '\n'
    string = string + XO(matriz[1][0]) + " " + XO(matriz[1][1]) + " " + XO(matriz[1][2]) + '\n'
    string = string + XO(matriz[2][0]) + " " + XO(matriz[2][1]) + " " + XO(matriz[2][2]) + '\n'
    return string 

turn = 0
fim = False

def solicitar_jogada(client_socket):
    mensagem = 'FAÇA A JOGADA ' + str(turn + 1) + ': '
    #Criptografa a mensagem
    mensagemCripto = fernet.encrypt(mensagem.encode('utf-8'))
    #Envia a mensagem criptografada
    client_socket.sendall(mensagemCripto)

while True:
    try:
        while not fim:
            client_socket = clients[turn % 2]
            jogadorDaRodada = ''
            if turn % 2 == 0:
                jogadorDaRodada = '1'
            else:
                jogadorDaRodada = '2'
            
            solicitar_jogada(client_socket)
            
            #Recebe os dados do cliente
            data = client_socket.recv(1024)

            if not data:
                #O cliente desconectou
                print('Cliente desconectado:', client_socket.getpeername())
                break

            jogadaDecriptada = fernet.decrypt(data)

            message = jogadaDecriptada.decode('utf-8')

            jogada = json.loads(message)
            l = jogada['linha']
            c = jogada['coluna']

            if turn == 9:
                print("Velha")
                msgVelha = fernet.encrypt(('\0'+"Deu Velha!").encode('utf-8'))
                clients[0].sendall(msgVelha)
                clients[1].sendall(msgVelha)

            else:

                print("jogada ", turn + 1)
                print('Jogada recebida: ', l, c)
                linha = l
                coluna = c
                if matriz[l][c] == 0:
                    matriz[l][c] = pow(-1, turn + 1)
                    matrix = printm(turn)
                    print(matrix)
                    matrixCripto = fernet.encrypt(('\0'+matrix +'\0').encode('utf-8'))                   
                    clients[0].sendall(matrixCripto)
                    clients[1].sendall(matrixCripto)
                    if Teste():
                        print("O ganhador é o jogador:", jogadorDaRodada)
                        ganhadorCripto = fernet.encrypt(('\n' + "O ganhador é o jogador:" + jogadorDaRodada).encode('utf-8'))
                        clients[0].sendall(ganhadorCripto)
                        clients[1].sendall(ganhadorCripto)

                        fim = True
                    turn += 1
                else:
                    print("Localização já preenchida")
                    avisoCripto = fernet.encrypt(('O jogador ' + jogadorDaRodada + ' tentou uma posição ocupada').encode('utf-8'))
                    clients[0].sendall(avisoCripto)
                    clients[1].sendall(avisoCripto)
                
                    

    except json.JSONDecodeError:
        print('Erro ao decodificar a mensagem JSON.')
    except KeyError:
        print('Chaves "linha" e "coluna" não encontradas na mensagem.')

    #Fecha a conexão com os clientes e o socket do servidor
    for client_socket in clients:
        client_socket.close()
    server_socket.close()
