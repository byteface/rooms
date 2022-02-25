
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from domonic.html import *
from functools import lru_cache

import os
# from domonic.html import *
from domonic.xml.aframe import *
from domonic.CDN import *

_scripts = script("""
AFRAME.registerComponent("foo", {
    init: function() {
      this.portals = document.querySelectorAll('a[href]') // TODO - use a class?
      //this.box = document.querySelector('a-box')
      //this.text = document.querySelector("a-text")
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

      //let boxPos = this.box.object3D.position
      //this.text.setAttribute("value", camPos.distanceTo(boxPos))
      //window.console.log(camPos.distanceTo(boxPos))

      // if the distance is less than 1.5 follow the url
      //if(camPos.distanceTo(boxPos)<1.5){ 
        //window.console.log(this.box.getAttribute('href'))
        // if it leaves our server pop up and tells the user the are going to load someone elses server
        //window.location = this.box.getAttribute('href')
      //}

    }
})
""")

# wrapper for all pages
_webpage = lambda scene: html(head(
    script(
        _src=CDN_JS.AFRAME_1_2),
        _scripts
    ),
    body(
    link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MARX),
    str(scene)
    )
)

# lobby
_scene = scene(
      box(_position="-10 0.5 -3", _rotation="0 45 0", _color="#4CC3D9", _href="/home"),
      sphere(_position="0 1.25 -5", _radius="1.25", _color="#EF2D5E", _href="/room"),
      cylinder(_position="1 0.75 -3", _radius="0.5", _height="1.5", _color="#FFC65D"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),
      sky(_color="#ECECEC"),
      '<a-camera foo><a-camera>', # TOOD - domonic can't do 'no attribute'
    )

# default home without a user edit
_home = scene(
      box(_position="-1 0.5 -5", _rotation="45 45 0", _color="#4CC3D9", _href="/"),
      sphere(_position="2 1.25 -5", _radius="1.25", _color="#EF2D5E"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),
      sky(_color="#ECECEC"),
      '<a-camera foo><a-camera>',
    )


app = FastAPI()

# lobby
@lru_cache
@app.get("/")
def root():
    return HTMLResponse(str(
        _webpage(_scene)
    ))

# users own room. editable
@lru_cache
@app.get("/home")
def home(username=None):
    return HTMLResponse(str(
        _webpage(_home)
    ))

@app.get("/room")
def room():
    room = scene(
      box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),
      sky(_color="#ECECEC"),
      '<a-camera foo><a-camera>',
    )
    return HTMLResponse(str(
        room
    ))

# generate a random room
@app.get("/random")
def random_room():
    room = scene(
      box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9"),
      # plane(_position="0 0 -4", _rotation="-90 0 0", _width="40", _height="4", _color="#7BC8A4"),
      sky(_color="#ECECEC"),
      '<a-camera foo><a-camera>',
    )
    return HTMLResponse(str(
        room
    ))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
