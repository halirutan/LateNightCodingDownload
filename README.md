# Download script for Jens Krüger's Late Night Coding sessions

Downloads all files of one of the toy project written during [C++ Jens' streams](https://www.twitch.tv/jhkrueger).
It works by downloading the `makefile` first and then trying to stupidly tracking all dependencies.
The script **overwrites** existing files and it only tracks dependencies coming from the `makefile` and downloaded
`cpp` files.

## Usage

Make sure you have all the requirements and you're using Python > 3.7

```shell script
pip install -r requirements.txt
```

Create an empty directory and change to it. Then call the script with the name of the project

```
mkdir OpenGL
cd OpenGL
path/to/LateNightCodingDownload.py OpenGL
```

