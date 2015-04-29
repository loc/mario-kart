Best Mario Kart Wii CV EVER

# OSX Install
## Prereqs
Install:
  - [brew](http://brew.sh/)
  - python [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Installing

Use `brew` to install opencv packages
```
brew tap homebrew/science
brew install opencv
```

Setup python
```
virtualenv kart
source kart/bin/activate
pip install -r requirements.txt
cd kart/lib/python2.7/site-packages/
ln -s /usr/local/Cellar/opencv/*/lib/python2.7/site-packages/cv.py cv.py
ln -s /usr/local/Cellar/opencv/*/lib/python2.7/site-packages/cv2.so cv2.so
```

Sample movies
```
./getVideos.sh
```

Run the program
```
python read.py bowsers-castle.mp4
```

# To use with streaming
nginx has a nice rtmp server that can allow redirecting and incoming streams.

Setup nginx with `brew` and setup a config
```
brew install nginx-full --with-rtmp-module
cat <<EOF > /usr/local/etc/nginx/servers/kart.conf
rtmp {
        server {
                listen 1935;
                chunk_size 4096;
                application castle {
                        play /path/to/mario-kart;
                }
        }
}
EOF
```

Start nginx 
```
nginx
```

You can stop with 
```
nginx -s stop
```

Make sure you can watch the video:
```
brew install mplayer
mplayer rtmp://127.0.0.1:1935/castle/bowsers-castle.mp4
```

Read from the stream:
```
python read.py rtmp://127.0.0.1:1935/castle/bowsers-castle.mp4
```
