import os
import config

print ("\n\n\n============ DETECCIÓN DE ROSTROS EN VÍDEOS ===========")


def showMenu():
    print ("1 - Detectar rostros en un vídeo en local")
    print ("2 - Detectar rostros en un vídeo de youtube")
    print ("3 - Detectar rostros en un directo de twitch")
    print ("4 - Detectar rostros usando la webcam")
    print ("5 - Detectar rostros en imágenes")

option = -1
while option < 0 or option > 5:
    try:
        showMenu()
        option = int(input("Introduce una opción: "))
    except ValueError:
        print("¡El valor debe ser un entero!\n")
        option = -1

if option == 1:
    print("Detectando rostros en vídeo situado en el archivo config...")
    os.system("python3 video_detector.py -v")
    
elif option == 2:
    link = str(input("Introduzca enlace: "))
    os.system("python3 video_detector.py -y {}".format(link))
    print(link)
elif option == 3:
    link = str(input("Introduzca enlace: "))
    os.system("python3 video_detector.py -t {}".format(link))
    print(link)
elif option == 4:
    print("Arrancando detección en webcam...")
    os.system("python3 video_detector.py -w")
elif option == 5:
    print("Arrancando detección sobre imagenes...")
    os.system("python3 image_detector.py")
    print("Las detecciones se han realizado correctamente en la ruta: {}".format(config.PATH_TO_OUTPUT_IMAGES))