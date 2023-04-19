import cv2

#converte a imagem para RGB.
def imagem_video_rgb(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb

#converte a imagem para HSV.
def imagem_video_hsv(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return hsv

#Cria uma janela onde o vídeo irá rodar.
cv2.namedWindow("checkpoint")
video = cv2.VideoCapture("video.mp4")

#Se o vídeo estiver rodando, ele continua exacutando o script
if video.isOpened(): 
    rval, frame = video.read()
#Se o vídeo não estiver rodando, o script para
else:
    rval = False

while rval:



    #Leitura do vídeo, frame a frame.
    rval, frame = video.read()
    #Caso a tecla ESC for pressionada, o vídeo para. 
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    
#Destroí a janela criada e para de executar o vídeo.
cv2.destroyWindow("checkpoint")
video.release()
