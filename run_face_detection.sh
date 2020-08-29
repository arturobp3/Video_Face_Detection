docker cp config.py $(docker ps -aqf "name=face_detection_app"):/code/config.py
docker cp ./images/. $(docker ps -aqf "name=face_detection_app"):/code/images
docker cp ./videos/. $(docker ps -aqf "name=face_detection_app"):/code/videos
docker start -a -i $(docker ps -aqf "name=face_detection_app")
rm -rf outputImages
rm -rf detectedFaces.avi
docker cp $(docker ps -aqf "name=face_detection_app"):/code/outputImages outputImages
docker cp $(docker ps -aqf "name=face_detection_app"):/code/detectedFaces.avi detectedFaces.avi
