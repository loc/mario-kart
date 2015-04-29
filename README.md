Best Mario Kart Wii CV EVER

# OSX Install
## Prereqs
Install brew
Install python virtualenv

## Installing

brew packages...
```
brew install nginx-full --with-rtmp-module
brew install
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

Setup nginx
```
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
