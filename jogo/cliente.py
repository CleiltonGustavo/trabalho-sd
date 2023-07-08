import socket

# Criação do socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexão com o servidor
server_address = ('127.0.0.1', 12345)  # exemplo de endereço e porta do servidor
sock.connect(server_address)

# Funções e código anterior omitidos por brevidade

def enviar_jogada(linha, coluna):
    # Envio da requisição para o servidor
    message = str(linha) + ' ' + str(coluna)
    sock.send(message.encode('utf-8'))

    # Recebimento da resposta do servidor
    response = sock.recv(1024).decode('utf-8')
    return response

# Jogo da velha
matriz = [[0,0,0],[0,0,0],[0,0,0]]

st = ""

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
        if( l == 3 or l == -3):
            st = "linha " + str(i)
            x = l
            return True
        else:
          c = Coluna(i)
          if(c == 3 or c == -3):
              st = "coluna " + str(i)
              x = c
              return True

    dp  = DiagP()
    if(dp == 3 or dp == -3):
        st = "Diagonal principal"
        x = dp
        return True
    else:
        ds = DiagS()
        if(ds == 3 or ds == -3):
            st = "Diagonal secundaria"
            x = ds
            return True
               
    
    return False


def XO(aux):
    if(aux == 0):
        return '.'
    elif(aux == -1):
        return 'X'
    elif(aux == 1):
        return 'O'

def printm():
    print(XO(matriz[0][0])," ",XO(matriz[0][1])," ",XO(matriz[0][2]))
    print(XO(matriz[1][0])," ",XO(matriz[1][1])," ",XO(matriz[1][2]))
    print(XO(matriz[2][0])," ",XO(matriz[2][1])," ",XO(matriz[2][2]))
    

aux = 0
a= 0
fim = False
while(fim == False):
    for i in range(10):
        if i == 9:
            print("Velha")
        else:    
            print("Vez do jogador ", aux+1)
            linha =int(input("Digite a linha : "))
            coluna = int(input("Digite a coluna : "))
            if(matriz[linha][coluna] == 0):
                matriz[linha][coluna] = pow(-1,aux+1)
                printm()
                if Teste():
                    print("ganhador eh o jogador : " + str(aux+1) )
                    fim = True
                aux = (aux+1)%2  
                break  
            else:
                print("Localizaçao estah preenchida")
        i = i+1        

# Fechamento da conexão
sock.close()
