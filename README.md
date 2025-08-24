# VideoToSpritesheetMaker

A simple tool to convert video animations to spritesheets quickly. This is useful when you want to utilize certain animations but save on resources by rendering them through a spritesheet rather than playing videos on screen. Particularly important in Unity3D since it is very weak in video performance.

Note: By default I've enabled chroma key to remove green screen from the video during generation.

It runs FFmpeg commands, so you will need to install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) before trying to run this code.
