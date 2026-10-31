from pacman import *
import time

def obtem_direecao(ponto1, ponto2):
    theta = math.atan2(ponto1[1] - ponto2[1], ponto1[0] - ponto2[0])
    dir_x = math.cos(theta)
    dir_y = math.sin(theta)
    return dir_x, dir_y

def pacman_cima(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (0, 5)

def pacman_baixo(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (0, -5) 

def pacman_direita(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (5, 0)  

def pacman_esquerda(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (-5, 0) 

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimenta_inky(estado_jogo):
    if 'direcao_atual' in estado_jogo['fantasmas'][INKY_OBJECT]:
        ultima_direcao = estado_jogo['fantasmas'][INKY_OBJECT]['direcao_atual']
    else:
        ultima_direcao = None

    direcoes_validas = [u for u in DIRECOES_POSSIVEIS if not ultima_direcao or u != (-ultima_direcao[0], -ultima_direcao[1])]
    nova_direcao = random.choice(direcoes_validas)

    estado_jogo['fantasmas'][INKY_OBJECT]['direcao_atual'] = nova_direcao

    return nova_direcao


def movimenta_blinky(estado_jogo):
    if 'direcao_atual' in estado_jogo['fantasmas'][BLINKY_OBJECT]:
        ultima_direcao = estado_jogo['fantasmas'][BLINKY_OBJECT]['direcao_atual']
    else:
        ultima_direcao = None

    direcoes_validas = [i for i in DIRECOES_POSSIVEIS if not ultima_direcao or i != (-ultima_direcao[0], -ultima_direcao[1]) ]
    nova_direcao = random.choice(direcoes_validas)

    estado_jogo['fantasmas'][BLINKY_OBJECT]['direcao_atual'] = nova_direcao

    return nova_direcao

def movimenta_pinky(estado_jogo):
    pos_pacman = estado_jogo['pacman']['objeto'].pos()
    pos_pinky = estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].pos()
    y_pacman = int(pos_pacman[1])
    x_pacman = int(pos_pacman[0])
    y_pinky = int(pos_pinky[1])
    x_pinky = int(pos_pinky[0])
    if x_pacman < x_pinky:
        if y_pacman < y_pinky:
            direcao_pinky = random.choice([1,3]) #0-cima,1-baixo,2-direita,3-esquerda
        elif y_pacman == y_pinky:
            direcao_pinky = random.choice([3,0,1])
        else:
            direcao_pinky = random.choice([0,3])
    elif x_pacman == x_pinky:
        if y_pacman < y_pinky:
            direcao_pinky = random.choice([1,2,3])
        elif y_pacman == y_pinky:
            direcao_pinky = random.choice([0,1,2,3])
        else:
            direcao_pinky = random.choice([0,2,3])
    else:
        if y_pacman < y_pinky:
            direcao_pinky = random.choice([1,2])
        elif y_pacman == y_pinky:
            direcao_pinky = random.choice([2,0,1])
        else:
            direcao_pinky = random.choice([0,2,3])

    return DIRECOES_POSSIVEIS[direcao_pinky]


def movimenta_clyde(estado_jogo):
    pos_pacman = estado_jogo['pacman']['objeto'].pos()
    pos_clyde = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()

    y_pacman = int(pos_pacman[1])
    x_pacman = int(pos_pacman[0])
    y_clyde = int(pos_clyde[1])
    x_clyde = int(pos_clyde[0])

    distancia = math.sqrt((x_pacman - x_clyde)**2 + (y_pacman - y_clyde)**2)
    scatter_distance_threshold = 100

    if distancia > scatter_distance_threshold:  
        if x_pacman < x_clyde:
            if y_pacman < y_clyde:
                direcao_clyde = random.choice([1, 3])  
            elif y_pacman == y_clyde:
                direcao_clyde = random.choice([3,0,1])  
            else:
                direcao_clyde = random.choice([0, 3])  
        elif x_pacman == x_clyde:
            if y_pacman < y_clyde:
                direcao_clyde = random.choice([1,2,3])
            elif y_pacman == y_clyde:
                direcao_clyde = random.choice([0, 1, 2, 3]) 
            else:
                direcao_clyde = random.choice([0,2,3])  
        else:
            if y_pacman < y_clyde:
                direcao_clyde = random.choice([1, 2])  
            elif y_pacman == y_clyde:
                direcao_clyde = random.choice([2,0,1])  
            else:
                direcao_clyde = random.choice([0, 2, 3]) 
    else: 
        if x_pacman < x_clyde:
            if y_pacman < y_clyde:
                direcao_clyde = random.choice([0, 2]) 
            elif y_pacman == y_clyde:
                direcao_clyde = random.choice([2,1,0]) 
            else:
                direcao_clyde = random.choice([1, 2]) 
        elif x_pacman == x_clyde:
            if y_pacman < y_clyde:
                direcao_clyde = random.choice([0,3,2])  
            elif y_pacman == y_clyde:
                direcao_clyde = random.choice([0, 1, 2, 3])  
            else:
                direcao_clyde = random.choice([1,3,2])
        else:
            if y_pacman < y_clyde:
                direcao_clyde = random.choice([0, 3]) 
            elif y_pacman == y_clyde:
                direcao_clyde = random.choice([3,1,0])  
            else:
                direcao_clyde = random.choice([1, 3])  

    return DIRECOES_POSSIVEIS[direcao_clyde]


def perdeu_jogo(estado_jogo):
    pacman_objeto = estado_jogo['pacman']['objeto']

    for fantasma in estado_jogo['fantasmas'].values():
        if ha_colisao(pacman_objeto, fantasma['objeto']):
            terminar_jogo(estado_jogo)
            return True

    return False


def atualiza_pontos(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor()
    y = estado_jogo['pacman']['objeto'].ycor()
    index = offset((x, y))
    if estado_jogo['mapa'][index] == 1:
        estado_jogo['score'] += 1
        estado_jogo['mapa'][index] = 7
        x_marcador, y_marcador = calcula_x_y_from_index(index)
        estado_jogo['marcador'].goto(x_marcador + 10, y_marcador + 10)
        estado_jogo['marcador'].dot(2, 'blue') 
        update_board(estado_jogo)



def atualiza_mapa(estado_jogo, x, y, elemento):
    index = offset((x,y))
    while estado_jogo['mapa'][index] in [BLINKY_OBJECT, PINKY_OBJECT, INKY_OBJECT, CLYDE_OBJECT]:
        index += 1
    estado_jogo['mapa'][index] = elemento

def actualiza_posicao_pacman_fantasma(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor() 
    y = estado_jogo['pacman']['objeto'].ycor()
    atualiza_mapa(estado_jogo, x, y, PACMAN_OBJECT)
    for ghost_id, ghost in estado_jogo['fantasmas'].items():
        x = ghost['objeto'].xcor()
        y = ghost['objeto'].ycor()
        atualiza_mapa(estado_jogo, x, y, ghost_id)


def guarda_jogo(estado_jogo):
    nome_ficheiro = r'C:\Users\diogo\OneDrive\Ambiente de Trabalho\pacman\Codigo-Alunos\save.txt'

    mapa_save = estado_jogo['mapa'][:]

    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    pacman_index = offset(pacman_pos)
    mapa_save[pacman_index] = 2 

    for fantasma_id, fantasma in estado_jogo['fantasmas'].items():
        fantasma_pos = fantasma['objeto'].pos()
        fantasma_index = offset(fantasma_pos)
        mapa_save[fantasma_index] = fantasma_id 

    with open(nome_ficheiro, 'w') as arquivo:
        for i in range(MAP_WIDTH):
            linha = mapa_save[i * MAP_WIDTH:(i + 1) * MAP_WIDTH]
            linha_str = ','.join(map(str, linha))
            arquivo.write(linha_str + '\n')

    print(f"Jogo salvo com sucesso")

def ganhar_jogo(estado_jogo):
    if estado_jogo['score'] >= 155:
        print("Parabéns! Você ganhou o jogo!")
        terminar_jogo(estado_jogo) 
        return True
    return False


def carrega_jogo(estado_jogo, nome_ficheiro):
    with open(nome_ficheiro, 'r') as mapa_inicial:
        mapa = [] 
        for linha in mapa_inicial:
            linha = linha.strip() 
            celulas = linha.split(',')  
            for celula in celulas:
                if celula.strip(): 
                    mapa.append(int(celula))  
        estado_jogo['mapa'] = mapa 


if __name__ == '__main__':
    try:
        funcoes_jogador = {'pacman_cima': pacman_cima, 'pacman_baixo': pacman_baixo, 'pacman_esquerda': pacman_esquerda, 'pacman_direita': pacman_direita, 'guarda_jogo' : guarda_jogo, 'carrega_jogo' : carrega_jogo}    
        funcoes_fantasmas = {BLINKY_OBJECT : movimenta_blinky, PINKY_OBJECT : movimenta_pinky, INKY_OBJECT : movimenta_inky, CLYDE_OBJECT : movimenta_clyde}


        nome_ficheiro = input('Pretende carregar um mapa (Enter para carregar o mapa default): ')
        if nome_ficheiro == '':
            nome_ficheiro = r'C:\Users\diogo\OneDrive\Ambiente de Trabalho\pacman\Codigo-Alunos\mapa_inicial.txt'

        estado_jogo = init_state()
        carrega_jogo(estado_jogo, nome_ficheiro)    
        setup(estado_jogo, True, funcoes_jogador,funcoes_fantasmas)

        while not perdeu_jogo(estado_jogo):
            if estado_jogo['mapa'] is not None:
                estado_jogo['janela'].update()
                movimenta_objectos(estado_jogo)
                atualiza_pontos(estado_jogo)
                time.sleep(0.05)
            if ganhar_jogo(estado_jogo):
                time.sleep(0.05)
                break
    except TclError:
        pass





