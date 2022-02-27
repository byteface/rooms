
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from domonic.html import *
from functools import lru_cache

from domonic import domonic

import os
# from domonic.html import *
from domonic.xml.aframe import *
from domonic.CDN import *

_scripts = script("""
var username = "Player" + Math.round(Math.random()*1000);
var players = [];

AFRAME.registerComponent("foo", {
    init: function() {
      this.portals = document.querySelectorAll('.portal') // TODO - use a class?
      this.socket = new WebSocket('ws://0.0.0.0:8008'); // 0.0.0.0 is locahost ONLY. use 127.0.0.1 for testing later
      this.username = username;
//      alert(this.username);

        this.socket.onopen = function(e) {
            console.log("[open] Connection established");
            console.log("Sending to server");
            var package = {"username":this.username};
            //this.socket.send(JSON.stringify(package));
        };

        this.socket.onmessage = function(event) {
            var server_data = JSON.parse(event.data);
            // console.log(server_data);
            for (var key in server_data) {
                if (server_data.hasOwnProperty(key)) {
                    // console.log(key + " -> " + server_data[key]);
                    if(key != username){
                    //    console.log('THIS PLAYER IS NOT ME!', key, username);
                        
                        // if key not in players, add it
                        if(players.indexOf(key) == -1){    
                            var sceneEl = document.querySelector("a-scene");
                            var p = document.createElement("a-box");
                            p.setAttribute("color", "red");
                            p.setAttribute("id", key);
                            //console.log('THE DATA IS', server_data[key]);
                            //p.setAttribute("position", server_data[key]);
                            sceneEl.appendChild(p);
                            players.push(key);
                        }else{
                            //console.log('THIS PLAYER IS ME!', key, username);
                            var p = document.querySelector("#"+key);
                            p.setAttribute("position", server_data[key].position.x + " " + server_data[key].position.y + " " + server_data[key].position.z);
                            //console.log('GOT HIM!', server_data[key]);
                        }
                    }
                }
            }
        };

        this.socket.onclose = function(event) {
        if (event.wasClean) {
            alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        } else {
            // e.g. server process killed or network down
            // event.code is usually 1006 in this case
            alert('[close] Connection died');
        }
        };

        this.socket.onerror = function(error) {
        alert(`[error] ${error.message}`);
        };

    },
    tick: function() {  
      let camPos = this.el.object3D.position
      for( var i=0; i<this.portals.length; i++){
        let p = this.portals[i]
        if(camPos.distanceTo(p.object3D.position)<1.5){ 
            // if it leaves our server pop up and tells the user the are going to load someone elses server
            window.location = p.getAttribute('href')
        }
      }
      if (this.el.object3D) {
          //console.log("YAY",this.el.object3D);

            degToRad = function(degrees) {
                return degrees * Math.PI / 180;
            }
            radToDeg = function(radians) {
                return radians * 180 / Math.PI;
            }
            function send_package(username, player, socket){
               // console.log('send_package!',player.object3D);
                var position = player.object3D.position.clone();
                var rotation = radToDeg(player.object3D.rotation.y);
                // console.log(rotation);
                var package = {
                    "username":username,
                    "position":position,
                    "rotation":rotation
                }
                //socket.send(JSON.stringify(package));
                // only send if socket is open
                if(socket.readyState == 1){
                    socket.send(JSON.stringify(package));
                }
            }
            send_package(this.username, this.el, this.socket);
        }
    }
})



</script>



""")

# wrapper for all pages
_webpage = lambda scene: html(head(
    script(
        _src=CDN_JS.AFRAME_1_2),

        # this bugs the controls?
        # <script src="https://unpkg.com/aframe-fps-look-controls-component/dist/aframe-fps-look-controls-component.min.js"></script>

        # script(_src="//cdn.rawgit.com/donmccurdy/aframe-extras/v4.1.1/dist/aframe-extras.min.js"),
        script(_src="//cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.1/dist/aframe-extras.min.js"),
        script(_src="https://unpkg.com/aframe-room-component/dist/aframe-room-component.min.js"),

        _scripts
    ),
    body(
    link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MARX),
    str(scene)
    )
)

# lobby
_scene = scene(
      box(_position="-10 0.5 -3", _rotation="0 45 0", _color="#4CC3D9", _class="portal", _href="/home"),
      sphere(_position="0 1.25 -5", _radius="1.25", _color="#EF2D5E", _class="portal", _href="/room"),
      cylinder(_position="1 0.75 -3", _radius="0.5", _height="1.5", _color="#FFC65D"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),
      entity(_text="value: Welcome to the rooms. Go explore!", material="color: blue", _geometry="primitive: plane; width: 4; height: auto"),
      sky(_color="#ECECEC"),
      '<a-camera foo><a-camera>',
      **{"_device-orientation-permission-ui":"enabled: false"},
    )

# default home without a user edit
_home = scene(
      box(_position="-1 0.5 -5", _rotation="45 45 0", _color="#4CC3D9", _class="portal", _href="/"),
      sphere(_position="2 1.25 -5", _radius="1.25", _color="#EF2D5E"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),

        '''
        <rw-room position="-2 0 -2" material="color:#866">
            <rw-wall position="4 0 0"></rw-wall>
            <rw-wall position="4 0 4"></rw-wall>
            <rw-wall position="0 0 4"></rw-wall>
            <rw-wall position="0 0 0">
                <rw-doorhole id="holeA"></rw-doorhole>
                <rw-doorlink from="#holeA" to="#holeB" position="2.5 0 0"></rw-doorlink>
            </rw-wall>
        </rw-room>
        <rw-room position="0 0 -3">
            <rw-wall position=" 1 0 -1" material="color:#787"></rw-wall>
            <rw-wall position=" 1 0  1" material="color:#877">
                <rw-doorhole id="holeB"></rw-doorhole>
            </rw-wall>
            <rw-wall position="-1 0  1" material="color:#878"></rw-wall>
            <rw-wall position="-1 0 -1" material="color:#778"></rw-wall>
        </rw-room>
        ''',

      sky(_color="#ECECEC"),
      '<a-camera foo><a-camera>',
      **{"_device-orientation-permission-ui":"enabled: false"},
    )

app = FastAPI()

# lobby
# @lru_cache
@app.get("/")
def root():
    return HTMLResponse(str(
        _webpage(_scene)
    ))

# users own room. editable
# @lru_cache
@app.get("/home")
def home(username=None):
    return HTMLResponse(str(
        _webpage(_home)
    ))

@app.get("/room")
def room():
    room = scene(
      box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9", _href="/home"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="400", _height="400", _color="#7BC8A4"),
      sky(_color="#ECECEC"),
      # entity( _id="rig", **{"_movement-controls":"fly: true; speed: 0.3"}, _position="25 0 25"),
      # '<a-camera camera look-controls="pointerLockEnabled: true"><a-camera>',

    '''<a-entity movement-controls="fly: true">
      <a-entity camera position="0 1.6 0" look-controls></a-entity>
    </a-entity>'''

    )
    return HTMLResponse(str(
        _webpage(room)
    ))

# generate a random room (from a seed) i.e. /random?seed=123 would always make the same thing
@app.get("/random")
def random_room(seed=0):

    import random

    def seed_to_random_hex_colour(number):
        numByte = str.encode(str(number))
        from hashlib import sha256
        hashed = sha256(numByte).hexdigest()
        return "#" + hashed[:6]

    sky_color = seed_to_random_hex_colour(seed)
    floor_color = seed_to_random_hex_colour(seed+seed)
    # print(col)
    room = scene(
      box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9", _class="portal", _href="/random?seed="+str(random.randint(0,1000000))),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color=floor_color),
      sky(_color=sky_color),
      '<a-camera foo><a-camera>',
      **{"_device-orientation-permission-ui":"enabled: false"},
    )
    return HTMLResponse(str(
        _webpage(room)
    ))

# use svg as map
@app.get("/map")
def map(map: int = 1):
    # load svg
    with open(f"static/maps/map{map}.svg", "r") as f:
        svgcontent = f.read()
    mapdata = domonic.parseString(svgcontent)
    walls = mapdata.querySelectorAll("rect")
    walls3d = []
    # build the walls from the svg
    for w in walls:
        # print('sup!')
        b = box(
            _position=f"{int(float(w.getAttribute('x')))/100} 0 {int(float(w.getAttribute('y')))/100}",
            _rotation="0 0 0",
            _width=int(float(w.getAttribute('width'))/100),
            _height=int(float(w.getAttribute('height'))/100),
            _color="#000000",
            _class="wall",
            # _geometry="primitive: box; width: {w.getAttribute('width')}; height: {w.getAttribute('height')}; depth: 0.1",
        )
        walls3d.append(str(b))

    # print(walls3d)
    room = scene(
      # box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),
      ''.join(walls3d),
      sky(_color="#ECECEC"),
      '<a-camera camera><a-camera>',
      **{"_device-orientation-permission-ui":"enabled: false"},
    )
    return HTMLResponse(str(
        _webpage(room)
    ))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
