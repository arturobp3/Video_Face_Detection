# Código adaptado de la siguiente fuente: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/camera.html

import numpy as np
import os
import tensorflow as tf
import cv2
import argparse
import pafy as p
import config

from streamlink import Streamlink
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Se parsean los argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=False, help="Path to the video where you want to detect faces",
                action="store_true")
ap.add_argument("-w", "--webcam", required=False, help="Detect faces from the webcam", action="store_true")
ap.add_argument("-y", "--youtube", required=False, help="Url to the YouTube video where you want to detect faces")
ap.add_argument("-t", "--twitch", required=False, help="Url to the Twitch video where you want to detect faces")
args = vars(ap.parse_args())

# Se establece que opción se va a usar
modelOK = os.path.exists(config.MODEL_PATH)
videoOK = os.path.exists(config.PATH_VIDEO)
webcamOK = args["webcam"]
youtubeOK = args["youtube"]
twitchOK = args["twitch"]


def loadPlatform():
    """
    Permite cargar el vídeo de entrada y algunos parametros dependiendo de la opción escogida mediante comando.

    @return:  videoIN (Objeto del video de entrada creado), fps (Número de fotogramas por segundo del video)
    """
    videoIN = None
    fps = 20.0
    if videoOK:
        videoIN = cv2.VideoCapture(config.PATH_VIDEO)
        fps = videoIN.get(cv2.CAP_PROP_FPS)
    if webcamOK:
        videoIN = cv2.VideoCapture(0)
    if youtubeOK:
        '''video = p.new(args["youtube"])
        best = video.getbest(preftype="mp4")
        videoIN = cv2.VideoCapture()
        fps = videoIN.get(cv2.CAP_PROP_FPS)
        videoIN.open(best.url)'''
        session = Streamlink()
        streams = session.streams(args["youtube"])
        stream = streams['best'].url
        videoIN = cv2.VideoCapture(stream)
        fps = videoIN.get(cv2.CAP_PROP_FPS)
    if twitchOK:
        session = Streamlink()
        streams = session.streams(args["twitch"])
        stream = streams['best'].url
        videoIN = cv2.VideoCapture(stream)
        fps = videoIN.get(cv2.CAP_PROP_FPS)

    return videoIN, fps


def createOutputVideo(name, videoIN, fps):
    """
    Devuelve un vídeo de salida, en el cual se van a ver las detecciones, en base a un nombre dado y a un video de
    entrada y fps especificos. El vídeo se guardará en la raíz del proyecto

    @param name: Nombre del vídeo de salida
    @param videoIN: Video de entrada creado previamente
    @param fps: Número de fps a los que funciona el vídeo de entrada

    @return:  videoOUT (Objeto que simboliza el vídeo de salida)
    """
    frame_width = int(videoIN.get(3))
    frame_height = int(videoIN.get(4))
    videoOUT = cv2.VideoWriter(name + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (frame_width, frame_height))

    return videoOUT


def loadTensorFlowModel():
    """
    Carga el modelo de TensorFlow en memoria. Este modelo se escoge en el fichero de configuración "config.py"

    @return: detection_graph (Objeto simbolizando el grafo de detección a usar en cada fotograma),
            category_index (Indice perteneciente a la etiqueta que se va a mostrar en la detección)
    """
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(config.PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(config.PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=config.NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    return detection_graph, category_index


def displayInfoToUser(frame, frameNum, length):
    """
    Muestra información al usuario sobre la detección que se está realizando. Si está realizando la detección sobre un directo,
    mostrará las detecciones. En cambio, si lo hace sobre vídeo, además de mostrar las detecciones, mostrará un porcentaje
    indicando el progreso.

    @param frame: Fotograma que debe mostrarse
    @param frameNum: Número de fotogramas que se han procesado
    @param length: Número de fotogramas que tiene el vídeo.
    """

    cv2.imshow('object detection', cv2.resize(frame, (800, 600)))
    percentage = (100 * frameNum) / length
    if length > 0 and (frameNum % 100 == int(frameNum / 100)):
        print("[INFO]: " + "%.2f" % round(percentage, 2) + "%")


def performDetection(detection_graph, category_index, length):
    """
    Realiza el proceso de detección, desde la obtención del fotograma del vídeo en concreto, hasta la asignación de los marcos
    de detección asociados a cada rostro.

    @param detection_graph: Grafo de detección usado para inferir sobre fotogramas
    @param category_index: Indice que representa la etiqueta que debe mostrarse en la detección. "Face" en nuestro caso
    @param length: Número de fotogramas que tiene el vídeo.
    """

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            frameNum = 0
            while videoIN.isOpened():
                # Leemos un frame
                ret, frame = videoIN.read()
                if ret is True:
                    image_np_expanded = np.expand_dims(frame, axis=0)

                    # Obtiene el tensor de imagen
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Cajas de detección
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Puntuación de detección
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    # Clases que se pueden detectar
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    # Número de detecciones
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    # Realiza la detección
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections], feed_dict={image_tensor: image_np_expanded})

                    # Se dibuja el marco en el fotograma
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=4)

                    # Aumentamos el número de fotogramas procesados
                    frameNum += 1

                    # Mostramos al usuario las detecciones en pantalla y/o el porcentaje de procesado del video
                    displayInfoToUser(frame, frameNum, length)

                    # Guardamos el fotograma en el vídeo de salida que se va a generar
                    videoOUT.write(frame)

                    # Permite parar la ejecución si se pulsa "q" o Ctrl + C
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    # Si se ha perdido la conexión con Twitch o YouTube, vuelve a reconectar y leer fotogramas del directo
                    if twitchOK or youtubeOK:
                        loadPlatform()
                    else:
                        break
                    break


if __name__ == "__main__":
    if modelOK:
        # Cargamos la plataforma escogida con el comando
        videoIN, fps = loadPlatform()

        # Número de fotogramas del video
        length = int(videoIN.get(cv2.CAP_PROP_FRAME_COUNT))

        if videoIN.isOpened() is False:
            print("Ha habido un error al abrir el vídeo")
        else:
            # Se crea el vídeo de salida
            videoOUT = createOutputVideo("detectedFaces", videoIN, fps)

            # Se obtiene el grafo de detección
            detection_graph, category_index = loadTensorFlowModel()

            # Realiza el proceso de detección
            performDetection(detection_graph, category_index, length)


        videoIN.release()
        videoOUT.release()
        cv2.destroyAllWindows()
    else:
        print("La ruta del modelo no existe. Comprueba la configuracion en 'config.py'")
