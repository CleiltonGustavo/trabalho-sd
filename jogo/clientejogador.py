import socket
import json


def game_request():
    client_socket.sendto(str(1).encode(), (host, port))
    client_socket.sendto(name.encode(), (host, port))
    print("Aguarde seu oponente...\n\n\n")
    opponent, address = client_socket.recvfrom(1024)
    opponent = opponent.decode()
    player, address = client_socket.recvfrom(1024)
    player = player.decode()

    while True:
        vez, address = client_socket.recvfrom(1024)
        vez = int(vez.decode())
        tabuleiro, address = client_socket.recvfrom(1024)
        tabuleiro = json.loads(tabuleiro.decode())

        show_board(tabuleiro, opponent, player)

        if (vez != 7) and (vez == 1):
            jogada = False
            while not jogada:
                print("Digite a linha em que deseja jogar:")
                playL = int(input())
                print("Digite a coluna em que deseja jogar:")
                playC = int(input())
                if tabuleiro[playL][playC] == "":
                    tabuleiro[playL][playC] = player
                    show_board(tabuleiro, opponent, player)
                    jogada = True
                    client_socket.sendto(json.dumps(tabuleiro).encode(), (host, 8001))
                else:
                    print("O local escolhido é inválido!!")
                    print("Tente Novamente\n")
                    show_board(tabuleiro, opponent, player)
        elif vez == 7:
            msg, address = client_socket.recvfrom(1024)
            print(msg.decode())
            input()
            break


def show_board(tabuleiro, opponent, player):
    if player == "X":
        player_opponent = "O"
    else:
        player_opponent = "X"
    print(name+"("+player+")\t\t\t\t\t\t\t\t\t\t"+opponent+"("+player_opponent+")\n\t\t\t\t\t", end="")
    for c in range(0, 3):
        print("  " + str(c) + " ", end="")
    print("\n\t\t\t\t\t ", end="")
    print(" ___" * 3)
    l = 0
    for linha in tabuleiro:
        print("\t\t\t\t\t"+str(l), end="")
        for coluna in linha:
            if coluna == "":
                print("|___", end="")
            else:
                print("|_" + coluna + "_", end="")
        print("|")
        l += 1

def ranking():
    client_socket.sendto(str(3).encode(), (host, port))
    rank, address = client_socket.recvfrom(1024)
    rank = json.loads(rank.decode())
    rank_number = 1
    print("-----------------------------------------------------------------")
    print("|     RANK      |             JOGADOR              |  VITORIAS  |")
    print("-----------------------------------------------------------------")
    for user in rank:
        print("\t["+str(rank_number)+"] \t\t\t"+user["name"]+"                   "+str(user["wins"]))
        rank_number += 1
    input()


# Socket de Comunicação
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 8000
host = "127.0.0.1"
op = 0
while op != 1:
    print("-------------------------------")
    print("|    Jogador 1 vs Jogador 2   |")
    print("-------------------------------")
    print("| Digite um nome de Jogador:  |")
    print("-------------------------------")
    name = input()
    client_socket.sendto(str(0).encode(), ('127.0.0.1', port))
    client_socket.sendto(name.encode(), (host, port))
    op, address = client_socket.recvfrom(1024)
    op = int(op.decode())


while True:
    print("\n\n\n\n")
    print("-------------------------------")
    print("|    Jogador 1 vs Jogador 2   |")
    print("-------------------------------")
    print("| (1) - JOGAR                 |")
    print("| (2) - PLACARES              |")
    print("| (3) - SAIR                  |")
    print("-------------------------------")
    op = int(input())

    if op == 1:
        game_request()
    elif op == 2:
        ranking()
    elif op == 3:
        break
    else:
        pass
