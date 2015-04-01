To download the test videos (soon I'll set up an rsync...this was quicker):
```
./getVideos.sh
```

Thoughts:

I've implemented a Watcher class tonight. The idea is that you pass the coordinates of the part of the video frame you want to look at and fill in an update function determining what the Watcher does with that window. Also, you can turn on and off watchers based on predicates of the overall state. For example, only watch for items when mode="racing". Soon I want to allow individual watchers to limit their own frame rate and pixel resolution–the idea being that different watchers may need higher fidelty than others.
