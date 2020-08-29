docker build -t face_detection_app .
docker create -ti --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --name=face_detection_app face_detection_app
xhost +local:root
./run_face_detection.sh