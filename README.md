# test

테스트를 진행합니다.

## Env.
Build image (based on ubuntu 22.04, python 3.10.12):
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