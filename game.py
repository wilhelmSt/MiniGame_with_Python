import random

def cardsValue(card):
    if(card%10 == 0):
        return 3
    elif(card%11 == 0):
        if(card%5 == 0):
            return 7
        else:
            return 5
    elif(card%5 == 0):
        return 2
    else:
        return 1

def createDashboard():
    global dashboard
    dashboard = []
    dashboard.clear()
    dashboard = [[0]*6 for i in range(5)]
    
def printDashboard():
    print("\n")
    for line in dashboard:
        print(line)
    print("\n")

def createCards():
    global cards
    cards = []
    cards.clear()
    cards = list(range(1, 105))
    return cards

def removeCardsFromCards(cartas):
    for i in cartas:
        cards.remove(i)

def listDashboardCards():
    listarDashboardCards = []
    for line in range(len(dashboard)):
        for column in range(len(dashboard[line])):
            if(dashboard[line][column] != 0):
                listarDashboardCards.append(dashboard[line][column])
    return listarDashboardCards

def createPlayers(qtd_jogadores):
    global jogadores
    jogadores = []
    for i in range(qtd_jogadores):
        jogador = {
            "jogador": i+1,
            "cartas": None,
            "vida": 60
        }
        jogadores.append(jogador)

def isAlive():
    alive = True
    for jogador in jogadores:
        if jogador.get("vida") <= 0:
            alive = False
            break
    return alive

def haveCards():
    for jogador in jogadores:
        if(len(jogador.get("cartas")) == 0):
            return False
    return True

def removeCarta(carta):
    # Verificar se jogador tem a carta
    # Se tiver a carta, remover ela do jogador
    for jogador in jogadores:
        for cartasDoJogador in jogador.get("cartas"):
            if(carta == cartasDoJogador):
                jogador.get("cartas").remove(carta)

def removeVida(carta, vidaNegativa):
    for jogador in jogadores:
        for cartasDoJogador in jogador.get("cartas"):
            if(carta == cartasDoJogador):
                jogador["vida"] -= vidaNegativa

def replaceLine(carta):
    for jogador in jogadores:
        for cartasDoJogador in jogador.get("cartas"):
            if(carta == cartasDoJogador):
                return "Escolha qual linha deseja substituir"

def rodada():
    cartasJogadas = []
    for jogador in jogadores:
        print(jogador.get("cartas"))
        print("jogador", jogador.get("jogador"), "selecione sua carta jogada: ")
        testInput = True
        while(testInput):
            cartaJogador = int(input())
            if(cartaJogador in jogador.get("cartas")):
                cartasJogadas.append(cartaJogador)
                testInput = False
            else:
                print("Jogue uma carta da qual voce possui")
                continue                
    cartasJogadas.sort()

    # Receber a carta do jogador ----------------------------- OK
    # Criar lista com as cartas jogadas nessa rodada --------- OK
    # Remover a carta jogada da mão de cada jogador ---------- OK

    # Inserir as cartas no dashboard {
    # VERIFICAR EM QUAL LINHA CADA CARTA VAI ENTRAR ()
    # VERIFICAR SE A CARTA ENTROU NA COLUNA 6 ()
    # }
    
    for card in cartasJogadas:
        maior = 0
        # Percorre a matriz para encontrar o número sucessor da carta a ser inserida
        for line in range(len(dashboard)):
            for column in range(len(dashboard[line])):
                if(column < 5):
                    if(dashboard[line][column] > maior and dashboard[line][column] != 0 and 
                    dashboard[line][column] < card and dashboard[line][column+1] == 0):
                        maior = dashboard[line][column]
                else:
                    if(dashboard[line][column] > maior and dashboard[line][column] != 0 and 
                    dashboard[line][column] < card):
                        maior = dashboard[line][column]

        # Caso a carta jogada for menor que todas as cartas da matriz
        if(maior == 0):
            localLine = int(input(replaceLine(card)))
            localLine -= 1
            somaCardsValue = 0
            for i in range(len(dashboard[localLine])):
                if(dashboard[localLine][i] != 0):
                    somaCardsValue += cardsValue(dashboard[localLine][i])
                    dashboard[localLine][i] = 0

            removeVida(card, somaCardsValue)
            dashboard[localLine][0] = card
            removeCarta(card)
            continue
        

        for line in range(len(dashboard)):
            for column in range(len(dashboard[line])):
                if(dashboard[line][column] == maior):
                    if(column == 4):
                        somaCardsValue = 0
                        for i in range(len(dashboard[line])):
                            if(dashboard[line][i]):
                                somaCardsValue += cardsValue(dashboard[line][i])
                                dashboard[line][i] = 0
                                
                        removeVida(card, somaCardsValue)
                        dashboard[line][0] = card
                        removeCarta(card)
                    else:
                        dashboard[line][column+1] = card
                        removeCarta(card)

    
def reciveCards():
    for x in jogadores:
        listCard = []
        for i in range(10):
            o = cards[random.randint(0, len(cards)-1)]
            listCard.append(o)
            cards.remove(o)

        x.update({"cartas": listCard})

def dashboardCards():
    for i in range(5):
        dashboard[i][0] = cards[random.randint(0, len(cards))]
        cards.remove(dashboard[i][0])

def jogo():
    # --- Inicio do jogo ---
    #Criando o dashboard
    createDashboard()
    #Criando as cartas do jogo
    createCards()
    #Dando as cartas do dashboard
    dashboardCards()
    #Imprimir o cartas do dashboard
    printDashboard()
    
    #Definindo a quantidade de jogadores
    createPlayers(int(input("Quantidade de jogadores: ")))
    #Dando as cartas dos jogadores
    reciveCards()

    # --- Jogo (Fase rodadas) --- , a rodada se repete até que um jogador tenha toda sua vida perdida 
    #                               ou tenha ficado sem cartas
    while(isAlive() and haveCards()):
        while(isAlive() and haveCards()):
            rodada()
            for jogador in jogadores:
                print(jogador)
            printDashboard()
        
        if(not(isAlive())):
            maiorVida = 0
            for jogador in jogadores:
                if(jogador.get("vida") > maiorVida):
                    maiorVida = jogador.get("vida")

            for jogador in jogadores:
                if(maiorVida == jogador.get("vida")):
                    print("O jogador:", jogador.get("jogador"), "venceu o jogo")
            break

        if(not(haveCards())):
            createCards()
            createDashboard()
            dashboardCards()
            printDashboard()
            removeCardsFromCards(listDashboardCards())
            reciveCards()
            continue

if(__name__ == "__main__"):
    jogo()  