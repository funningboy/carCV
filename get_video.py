
import os
import subprocess

def get_video():
    """ get video source """
    ckout = 'svn checkout http://opencv-lane-vehicle-track.googlecode.com/svn/trunk/ opencv-lane-vehicle-track-read-only'
    proc = subprocess.Popen(ckout, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    id(proc)
    proc.wait()

def setup_video():
    """ setup video path """
    run = 'mv ./opencv-lane-vehicle-track-read-only/bin/road.avi ./data'
    proc = subprocess.Popen(run, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    id(proc)
    proc.wait()

def main():
    get_video()
    setup_video()

if __name__ == '__main__':
    main()
