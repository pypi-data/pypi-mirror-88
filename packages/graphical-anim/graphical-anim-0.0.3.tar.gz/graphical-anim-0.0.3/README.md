# Graphical Animation
### A command line graphical animation creator.

## Features
* Linear interpolation in shape size, location, and color
* MP4 export

## How to use
1. Import the module:
    * `import graphical_anim as ganim`
2. Define a video:
    * `video = ganim.Video(resolution, fps)`
3. Add a layer (a rectangle in this example):
    * `rect = ganim.shapes.Rect(location, size, color)`
4. Insert keyframes:
    * `rect.keyframe(frame, datapath, value)`
    * Example: `rect.keyframe(10, "loc_x", 2.3)`

## Changelog
Version 0.0.3
* Circle and polygon
* Fixed minor bugs.

Version 0.0.2
* First working version
* Rectangle and export video.