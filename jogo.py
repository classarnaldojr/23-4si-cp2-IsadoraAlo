import cv2
import numpy as np

#Cor padrão para desenhos e textos.
roxinho = (115, 50, 168)

placar = [0, 0]

frame_por_segundo = 0

#Converte a imagem para HSV
def imagem_para_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#Acha o range de cores das mãos
def achar_cores(hsv):
    mask_hsv_rosa = cv2.inRange(hsv, np.array([0, 20, 0]), np.array([255, 255, 255]))
    mask_hsv_amarelo = cv2.inRange(hsv, np.array([0, 30, 0]), np.array([255, 255, 255]))
    return cv2.bitwise_or(mask_hsv_amarelo, mask_hsv_rosa)

#Define os contornos da imagem
def acha_contorno(hsv):
    contornos, _ = cv2.findContours(achar_cores(hsv), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return sorted(contornos, key=cv2.contourArea, reverse= True)

#Retorna o valor numérico da área do contorno
def acha_area_contorno(contorno):
    return cv2.contourArea(contorno)

#Desenha o contorno em torno da imagem
def desenha_contorno(rgb, contornos):
    contornos_img = rgb.copy()
    return cv2.drawContours(contornos_img, [contornos[0], contornos[1]], -1, roxinho, 5)

#Identifica o tipo movimento
def identifica_movimento(area):
    if(50000 < area < 52000):
        return 'Pedra'
    if(63000  < area < 64000):
        return 'Papel'
    if(48000 < area < 49500):
        return 'Tesoura'

#Imprime na tela um texto
def exibe_texto(txt, y):
    return cv2.putText(desenho_contornos, str(txt),(50,y), cv2.FONT_HERSHEY_SIMPLEX,1, roxinho,2,cv2.LINE_AA)

#Calcula o centro de massa do objeto.
def centro_do_objeto(contorno):
    return int(cv2.moments(contorno)['m10']/cv2.moments(contorno)['m00']) + int(cv2.moments(contorno)['m01']/cv2.moments(contorno)['m00'])

#Identifica a posição do jogador
def identifica_jogador(contornos):
    if (centro_do_objeto(contornos[0]) < centro_do_objeto(contornos[1])):
        jogador1 = contornos[0]
        jogador2 = contornos[1]
    else:
        jogador1 = contornos[1]
        jogador2 = contornos[0]        
    return jogador1, jogador2

#Identifica o jogador ganhador
def identifica_vitoria(movimento_1, movimento_2):
    if(movimento_1 == movimento_2):
        return 'Empate'
    elif(movimento_1 == 'Pedra'):
        if movimento_2 == "Tesoura":
            return 'Jogador 1 ganhou!'
        else:
            return 'Jogador 2 ganhou!'
    elif(movimento_1 == 'Papel'):
        if movimento_2 == "Pedra":
            return 'Jogador 1 ganhou!'
        else:
            return 'Jogador 2 ganhou!'
    elif(movimento_1 == 'Tesoura'):
        if movimento_2 == "Papel":
            return 'Jogador 1 ganhou!'
        else:
            return 'Jogador 2 ganhou!'
        
def calcula_placar(resultado):
    if(frame_por_segundo % 85 == 0):  
        if(resultado == 'Jogador 1 ganhou!'):
            placar[0] += 1
        if(resultado == 'Jogador 2 ganhou!'):
            placar[1] += 1

cv2.namedWindow("checkpoint")
video = cv2.VideoCapture("pedra-papel-tesoura.mp4")

if video.isOpened(): 
    rval, frame = video.read()
else:
    rval = False
while rval:
    frame_por_segundo += 1

    hsv = imagem_para_hsv(frame)

    #Acha o contorno das mãos
    contornos = acha_contorno(hsv)
    #Desenha o contorno das mãos
    desenho_contornos = desenha_contorno(frame, contornos)

    #Identifica a posição dos jogadores na tela
    jogador1, jogador2 = identifica_jogador(contornos)

    #Calcula a area de contorno dos jogadores
    area_1 = acha_area_contorno(jogador1)
    area_2 = acha_area_contorno(jogador2)

    #Identifica o movimento dos jogadores
    movimento_1 = identifica_movimento(area_1)
    movimento_2 = identifica_movimento(area_2)

    resultado = identifica_vitoria(movimento_1,movimento_2)
    
    calcula_placar(resultado)

    #Imprime os movimentos realizado na tela
    ala = exibe_texto(movimento_1+' x '+movimento_2, 50)
    #Imprime na tela o placar
    ala = exibe_texto(str(placar), 100)
    #Imprime o resultado da partida na tela
    ala = exibe_texto(resultado, 150) 

    #Exibe a imagem scriptada.
    cv2.imshow("checkpoint", ala)

    rval, frame = video.read()
    key = cv2.waitKey(20)

    #Caso a tecla ESC for pressionada, o vídeo para. 
    if key == 27:
        break
cv2.destroyWindow("checkpoint")
video.release()
