import socket
import threading



#############################################################################################################################
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
            #print(velha)
            socketC1.send("Velha").encode("uft-8")
            socketC2.send("Velha").encode("uft-8")
        else:    
            #print("Vez do jogador ", aux+1)
            socketC1.send("Vez do Jogador ",aux+1).encode("uft-8")
            socketC2.send("Vez do Jogador ",aux+1).encode("uft-8")
            
             
            if(aux == 0):
                Socketx = SocketC1

            else:
                Socketx = SocketC2
            #linha =int(input("Digite a linha : "))    
            Socketx.send("Digite a linha : ").encode('utf-8'))
            msg = Socketx.recv(1024).decode('utf-8')
            
            #coluna = int(input("Digite a coluna : "))
            Socketx.send("Digite a coluna : ").encode('utf-8'))
            msg = Socketx.recv(1024).decode('utf-8')
                
            if(matriz[linha][coluna] == 0):
                matriz[linha][coluna] = pow(-1,aux+1)
                
                
                socketC1.send(printm()).encode('utf-8'))
                socketC2.send(printm()).encode('utf-8'))
                
                if Teste():
                    #print("ganhador eh o jogador : " + str(aux+1) )    
                    socketC1.send("ganhador eh o jogador : " + str(aux+1).encode('utf-8'))
                    socketC2.send("ganhador eh o jogador : " + str(aux+1).encode('utf-8'))
                    
                    fim = True
                aux = (aux+1)%2  
                break  
            else:
                Socketx.send("Localizaçao estah preenchida").encode("uft-8")
        i = i+1    


#############################################################################################################################





















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
 
    
