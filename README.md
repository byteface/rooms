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

[http://eventual.technology:9000/environment?preset=forest](http://eventual.technology:9000/environment?preset=forest)


note - not https

## notes

symlinking the servcies:
sudo ln -s ~/Desktop/rooms/multi.service /etc/systemd/system/multi.service
sudo systemctl start multi.service
