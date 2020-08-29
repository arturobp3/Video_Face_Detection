import os

'''
Permite asignar la ruta de un modelo para utilizarlo en la detección. Hay que cambiar el segundo parámetro de la función
 "join". Por defecto se usa en tiempo real.

Opciones:
----------------------------------------------------
En videos: "models/faster_inceptionResnet_videos/"
En tiempo real: "models/faster_inception_realtime/" 
----------------------------------------------------
'''
MODEL_PATH = os.path.join('./', 'models/faster_inception_realtime/')


'''
Permite asignar una ruta de un vídeo local sobre el que se quiera utilizar la detección facial. Se debe adjuntar el vídeo
en la carpeta 'videos' y cambiar el nombre en la constante. Por defecto, se ejecutará sobre un vídeo que proporcionamos
de prueba. El vídeo que se genere con las detecciones se guardará en la raíz del proyecto. 
'''
PATH_VIDEO = os.path.join('./videos/', 'joker.mp4')


'''
Permite asignar una ruta que indique la carpeta donde se encuentran las fotos sobre las que queremos realizar la detección
facial con el fichero 'image_detector.py'. Las imagenes deben ser en formato JPG. Por defecto se ha establecido en la carpeta
'images' que contiene unos ejemplos de prueba.
Además, se puede configurar una ruta para las imágenes de salida.
'''
PATH_TO_IMAGES = os.path.join('./', 'images/')
PATH_TO_OUTPUT_IMAGES = os.path.join('./', 'outputImages/')




'''
---------------------------------------------------------
ATENCION: Las siguientes constantes no se deben modificar
---------------------------------------------------------
'''
# Ruta al grafo de inferencia que se usa para realizar la detección
PATH_TO_CKPT = os.path.join(MODEL_PATH, 'frozen_inference_graph.pb')

# Ruta a las etiquetas que usa TensorFlow
PATH_TO_LABELS = os.path.join('./', 'face_label_map.pbtxt')

# Número de clases a detectar
NUM_CLASSES = 1

# Obtención del nombre de las imagenes en formato .jpg de la ruta que especifica el usuario
L = []
for n in os.listdir(PATH_TO_IMAGES):
    if n.endswith('jpg'):
        L.append(n)
L.sort()
IMAGES_PATH = [ os.path.join(PATH_TO_IMAGES, i) for i in L ]

# Tamaño de imagen necesario para 'image_detector.py'
IMAGE_SIZE = (12, 8)
