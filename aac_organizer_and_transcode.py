#!/usr/bin/python

import mutagen.mp4
import os
import shutil
import sys
import argparse
from unicodedata import normalize

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='A script to reorganize MP3/AAC files into directories sorted by Artist/Album into folders')
parser.add_argument('--fromPath', help='Path to directory of files for scanning', required=True)
parser.add_argument('--toPath', help='Path to output directory', required=True)
parser.add_argument('--bitRate', help='Desired AAC Average Bit Rate in kbps (example: 128)', default=128)
args = parser.parse_args()

tree = os.walk(args.fromPath)
for branch in tree:
    fileList = branch[2]
    currDir = branch[0]
    for filename in fileList:
        file_ext = os.path.splitext(filename)[1].lower().strip('.')
        if file_ext == 'm4a':
            s = ''
            filePath = os.path.join(currDir,filename)
            print ('FilePath: %s' % (filePath))
            try:
                metadata = mutagen.mp4.MP4(filePath)
            except mutagen.mp4.MP4StreamInfoError: 
                print ('File: %s encountered error' % (filename))
                break
            try:
                titleList = (metadata['\251nam'])
            except KeyError:
                print "Problem obtaining metadata - skipping"
                break
            title = s.join(titleList).replace(' ','_')
            try:
                artistList = metadata['\251ART']
            except KeyError:
                print "Problem obtaining metadata - skipping"
                break
            artist = s.join(artistList).replace(' ','_')
            try:
                albumList = metadata['\251alb']
            except KeyError:
                print "Problem obtaining metadata - skipping"
                break
            album = s.join(albumList).replace(' ','_')
            print ('Artist: %s - Album: %s - SongTitle: %s' % (artist, album, title))
            if "Compilations" in currDir:
                destination = u'%s/Compilations/%s/%s' % (args.toPath, album, filename)
            else:
                destination = u'%s/%s/%s/%s' % (args.toPath, artist, album, filename)
            #Do Transcode
            os.system('ffmpeg -i "' + filePath + '" -c:a aac -b:a ' + args.bitRate + 'k "/Volumes/Macintosh SSD/tmp/' + filename + '"')
            filePath = '/Volumes/Macintosh SSD/tmp/' + filename
            print ('Temp File Path: %s' % filePath)
            destDir = os.path.dirname(destination)
            if not os.path.exists(destDir):
                os.makedirs(destDir)
            if not os.path.isfile(destination):
                shutil.copyfile(filePath,destination)
                print ('Copying File - Source: %s\nDestination: %s\n' % (filePath,destination))
            else:
                print ('Skipping File - Destination: %s - **Already Copied\n' % (destination))
            os.remove(filePath)
