# rooms

A little weekend project idea.

Basically create 3d rooms with aframe and put hrefs on shapes to make them into portals to other rooms.

Walk into the shapes to go to other rooms which are just routes.

## Installation

```bash
pip install -r requirements.txt
. venv/bin/activate
python app.py
```

## Demo

Walk into the shapes to hyper link...

[http://eventual.technology:9000/](http://eventual.technology:9000/)

[http://eventual.technology:9000/random?seed=123](http://eventual.technology:9000/random?seed=123)

note - not https
note - doesn't have the socket multi socket on there yet. may try 2moro


## notes

I chucked the server files in there. rename service to .txt to read it. symlink it to ur systemd and enable it then it will run uvicorn in the background

multi-user mode - you will have pop 2 terminal windows and run multi.py in one of them.. then run the app. and open 2 browers and you will see the red squares moving around.