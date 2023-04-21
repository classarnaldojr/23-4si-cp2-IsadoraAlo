import cv2
import numpy as np

# cor padrão para desenhos e textos.
roxinho = (115, 50, 168)

#converte a imagem para RGB
def imagem_video_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#converte a imagem para HSV
def imagem_video_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#acha o range de cores das mãos
def achar_cores(hsv):
    mask_hsv_rosa = cv2.inRange(hsv, np.array([0, 20, 0]), np.array([255, 255, 255]))
    mask_hsv_amarelo = cv2.inRange(hsv, np.array([0, 30, 0]), np.array([255, 255, 255]))
    return cv2.bitwise_or(mask_hsv_amarelo, mask_hsv_rosa)

#define os contornos da imagem
def acha_contorno(hsv):
    contornos, _ = cv2.findContours(achar_cores(hsv), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return sorted(contornos, key=cv2.contourArea, reverse= True)

#retorna o valor numérico da área do contorno
def acha_area_contorno(contorno):
    return cv2.contourArea(contorno)

#desenha o contorno em torno da imagem
def desenha_contorno(rgb, contornos):
    contornos_img = rgb.copy()
    return cv2.drawContours(contornos_img, [contornos[0], contornos[1]], -1, roxinho, 5)

#identifica a imagem de movimento, e imprime o texto na tela
#def identifica_movimento(img, ref, minValue, maxValue, texto):
#identifica o jogador ganhador
#def identifica_vitoria:

#Cria uma janela onde o vídeo irá rodar.
cv2.namedWindow("checkpoint")
video = cv2.VideoCapture("pedra-papel-tesoura.mp4")

#Se o vídeo estiver rodando, ele continua exacutando o script
if video.isOpened(): 
    rval, frame = video.read()
#Se o vídeo não estiver rodando, o script para
else:
    rval = False

while rval:

    #converte a imagem para RGB
    rgb = imagem_video_rgb(frame)
    #converte a imagem para HSV
    hsv = imagem_video_hsv(frame)

    #acha o contorno das mãos
    contornos = acha_contorno(hsv)
    #desenha o contorno das mãos
    desenho_contornos = desenha_contorno(rgb, contornos)

    #calcula o centro de massa do primeiro jogador
    print(acha_area_contorno(contornos[0]))
    print(acha_area_contorno(contornos[1]))
    #calcula o centro de massa do segundo jogador
    # #Identifica o movimento pedra
    
    #Identifica o movimento papel
    
    # #Identifica o movimento tesoura
    

    #Exibe a imagem scriptada.
    cv2.imshow("checkpoint", desenho_contornos)

    #Leitura do vídeo, frame a frame.
    rval, frame = video.read()
    
    #Aguarda o pressionamento da tecla.
    key = cv2.waitKey(20)

    #Caso a tecla ESC for pressionada, o vídeo para. 
    if key == 27:
        break

#Destroí a janela criada e para de executar o vídeo.
cv2.destroyWindow("checkpoint")
video.release()
