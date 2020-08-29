# Detección de rostros en vídeos digitales: demostración
Este es una demostración de la capacidad de los modelos generados de poder detectar rostros en vídeos. Este repositorio forma parte del Trabajo de Fin de Grado realizado por estudiantes de Ingeniería Informática e Ingeniería del Software de la Facultad de Informática de la Universidad Complutense de Madrid en 2020.

Los miembros que forman parte de dicho grupo de trabajo son los siguientes:
+ Arturo Barbero Pérez
+ Alejandro Cabezas Garríguez
+ José Morcuende Sierra

En este documento se encuentra el manual de utilización de dicho código, así como el manual de instalación correspondiente. El documento se divide en los siguientes apartados:
1. **Manual de instalación**
2. **Manual de uso**

## 1. Manual de instalación
### 1.1 Linux (Recomendado)
Para sistemas Linux se realizará la instalación vía **Docker** para simplificarla. Por lo tanto, son necesarios los siguientes requisitos:
+ Docker (Versión 19.03 o superior): En [este enlace](https://docs.docker.com/engine/install/) podrás encontrar un manual de instalación de Docker orientado para los Sistemas Operativos de **CenOS, Debian, Fedora, Raspbian y Ubuntu**.

Para la instalación, lo primero que debemos realizar es descargar el repositorio, a través del gestor de descargas de GitLab o a través del siguiente comando:

        git clone http://gitlab.fdi.ucm.es/arturobp/facedetection_tfg.git

Lo siguientes que realizaremos será entrar en el directorio donde hemos descargado el repositorio:

        cd facedetection_tfg

Una vez situados en la carpeta, deberemos ejecutar el siguiente comando:

        ./init.sh

Dicho comando realizará todo el trabajo por nosotros. Una vez el proceso haya concluido, se iniciará la demostración, por lo que si se ha llegado a este punto es recomendable navegar al apartado del manual de uso. En caso de haber algún problema al utilizar Docker, podría intentarse también la instalación especificada para el sistema Windows, dado que también serviría para Linux.

### 1.2 Windows
Debido a diferentes problemas de compatibilidad, no ha sido posible realizar la instalación del software a través de **Docker**, por lo que realizaremos la instalación de manera manual. Para ello, necesitamos los siguientes requisitos:
+ Python (Versión 3.7): En [este enlace](https://www.python.org/downloads/release/python-370/) encontrarás la página oficial de python para poder descargarlo. La versióm debe ser de 64 bits.
+ Además, según la página de TensorFlow, se debe disponer de una tarjeta GPU NVIDIA con capacidad de procesamiento CUDA 3.5 o versiones posteriores. Es posible que esto pueda ocasionar futuros errores.

Una vez hemos descargado Python, debemos descargar el repositorio a través del gestor de descargar de GitLab o a través del siguiente comando si disponemos del cliente de GIT para windows (el cual puede descargarse a través del [siguiente enlace](https://git-scm.com/downloads))

    git clone http://gitlab.fdi.ucm.es/arturobp/facedetection_tfg.git

Una vez hemos descargado el repositorio, debemos acceder a él y, una vez dentro de la carpeta, deberemos abrir la consola de comandos de Windows y escribir el siguiente comando:
    
    pip install -r requirements.txt

Dicho comando importará todas las librerías necesarias para su ejecución. **Es muy importante** que a la hora de realizar el comando estemos situados dentro de la carpeta del repositorio, de lo contrario no funcionará.

Además, debemos introducir el siguiente comando para instalar la versión de TensowFlow no adaptada a GPU:

    pip install tensorflow==1.14.0

Una vez instaladas las librerías necesarias, el proceso de instalación habrá concluído y, por tanto, es recomendable situarse sobre el apartado de manual de uso.
 
## 2. Manual de uso

### 2.1 Contenido
El repositorio contiene varias imágenes y vídeos de prueba para que puedan ser usados sin necesidad de importarlos, de tal manera que se ahorra tiempo de cara a la ejecución. Dichos archivos si situan en las carpetas de `images` y `videos`.

También podemos encontrar los modelos generados, al igual que algunos archivos auxiliar usada para la creación de los marcos a la hora de pintar la detección en la imagen.

Por otro lado, encontraremos ficheros necesarios para la instalación y ejecución correcta, como son el `Dockerfile`, los script bash y otros.

Por último, encontraremos un archivo llamado `config.py`, donde se detallan las configuraciones que se pueden realizar sobre la demostración y que se deben cambiar **antes de arrancar la aplicación**. Para saber más detalles sobre este archivo, recomendamos entrar en él puesto que es ahí donde se indica todo lo necesario.

Al ejecutar la aplicación, nos encontraremos con la ventana principal de esta. Dicha ventana contiene un menú con las siguientes opciones:

1. Detectar rostros en un vídeo local
2. Detectar rostros en un vídeo de YouTube
3. Detectar rostros en una transmisión en directo de Twitch
4. Detectar rostros a través de la Webcam del ordenador
5. Detectar rostros en imágenes 

Si seleccionamos las opciones 2 y 3, nos pedirá un enlace, el cual debe ser o bien uno que conduzca a un vídeo o directo de YouTube o bien uno que nos lleve a un directo de Twitch. La opción 1 comenzará con la detección del vídeo situado en la carpeta de `videos`. Dicho vídeo puede cambiarse si ajustamos el parámetro apropiado dentro del archivo de configuración explicado anteriomente. Si seleccionamos la opción 4, la Webcam se activiará y podremos detectar rostros en tiempo real. Si seleccionamos la opción 5, las imágenes situadas en la carpeta `images` comenzarán a pasar por el detector. Una vez analizadas todas, los resultados se almacenarán dentro de la carpeta `outputImages` situada en la raiz de este proyecto y se creará cuando el proceso finalice.

**Importante**: El script `face_detection_init_script.py` contiene llamadas a scripts de python. Estas llamadas se realizan usando "python3 ...", pero podría ser que su sistema no cuente con dicho comando. Es por ello que puede modificarse el script para poner "python ..." y así evitar futuros problemas.

Para salir de cualquiera de las opciones, basta con pulsar `Ctrl + C` para poder salir de la aplicación. El resultado de la detección se almacenará en un archivo llamado `detectedFaces.avi` que se creará en la raíz de este repositorio cuando finalice la aplicación, bien por la finalización del vídeo en cuestión o bien por forzar su salida. Dicho archivo contiene el vídeo analizado.

### 2.2 Linux
Como hemos realizado la instalación a través de docker, una vez esta ha concluido nos encontramos con la pantalla principal de la aplicación. Si deseamos terminar la ejecución, basta con pulsar `Ctrl + C`. Si deseamos volver a ejecutarlo, unicamente deberemos ejecutar el siguiente comando:

    ./run_face_detections.sh

### 2.3 Windows
Para poder arrancar la aplicación y situarnos en la ventana principal de esta, deberemos ejecutar el siguiente comando una vez finalizada la instalación:

    python face_detection_init_script.py

### 2.4 Comandos
En caso de que la ejecución del script `face_detection_init_script.py` no haya funcionado por alguna razón, a continuación se muestran comandos que harán exactamente lo mismo que el script anterior, pero de una manera más gráfica:

    - python video_detector.py -v : Ejecuta el detector con el vídeo preconfigurado en el archivo config.py
    - python video_detector.py -y [URL] : Ejecuta el detector con vídeos de YouTube
    - python video_detector.py -t [URL] : Ejecuta el detector con retransmisiones de Twitch
    - python video_detector.py -w : Ejecutar el detector con la Webcam
    - python image_detector.py : Ejecuta el detector en imágenes situadas en la carpeta images.