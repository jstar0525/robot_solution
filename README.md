# robot_solution
Develop 3D point cloud data processing and projection system

## Env.
Build image (based on ubuntu 24.04, python 3.12.3):
```
docker build -t aiv:coding_test .
```

Once you have the image, start a container as follows:
```
docker run -it \
    -v /etc/localtime:/etc/localtime:ro \
    -e TZ=Asia/Seoul \
    -e QT_X11_NO_MITSHM=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -e DISPLAY=$DISPLAY \
    -v /home/jstar/test:/home/jstar/test \
    aiv:coding_test \
    bash
```
python 버전 : 3.12.3