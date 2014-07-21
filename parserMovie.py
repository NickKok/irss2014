import glob, codecs
import pysrt
import sys
import os
import logging
from srtmerge import srtmerge

logging.basicConfig(format='%(message)s', level=logging.INFO)


def readAllFiles(path):
  for root, dirs, files in os.walk(path):
    files.sort()
    for fileread in files:
      if fileread.endswith(".scenes"):
        with open(path + fileread) as a_file:
          lines = a_file.readlines()
          fileName = lines[0].rstrip()
          del lines[0]
          number = 1
          listSrt = list()
          for item in lines:
            lhs, rhs = item.split(",", 1)
            partName, ext = fileName.split(".", 1)
            newPath = path + 'parted/'
            if not os.path.exists(newPath):
              os.makedirs(newPath)
            newFileNameMovie = newPath + partName + '_' + str(number) + '.mp4'
            newFileNameSrt = newPath + partName + '_' + str(number) + '.srt'
            number += 1

            # Split movie file
            # ffmpeg -i video.mp4 -ss 00:01:00 -to 00:02:00 -c copy cut.mp4
            # ffmpeg -i input.avi -c:v libx264 -crf 19 -preset slow -c:a libfaac -b:a 192k -ac 2 out.mp4
            try:
              if ext == 'mp4':
                os.system('ffmpeg -i "%s" -ss "%s" -to "%s" -c copy "%s" ' % (
                  path + fileName, lhs, rhs.rstrip(), newFileNameMovie))
              else:
                os.system('ffmpeg -i "%s" -ss "%s" -to "%s" -c:v libx264 -c:a copy "%s" ' % (
                  path + fileName, lhs, rhs.rstrip(), newFileNameMovie))
            except:
              print "Error with spliting movie file"

            # Split *.srt file
            try:
              #subs = SubRipFile.open(path + partName + '.srt')
              try:
                subs = pysrt.open(path + partName + '.srt')
              except UnicodeDecodeError:
                subs = pysrt.open(path + partName + '.srt',encoding='iso-8859-1')
              Hs, Ms, Ss = lhs.split(":", 2)
              He, Me, Se = rhs.split(":", 2)
              part = subs.slice(starts_after={'hours': int(Hs), 'minutes': int(Ms), 'seconds': int(Ss)},
                                ends_before={'hours': int(He), 'minutes': int(Me), 'seconds': int(Se)})
              part.save(newFileNameSrt)
              listSrt.append(newFileNameSrt)
            # part.shift(hours=-int(Hs), minutes=-int(Ms), seconds=-int(Ss))
            except:
              print "Error with spliting srt file"
          if not listSrt:
            print "Error there are no srt files"
          else:
            """
            srtdir = path+'wholeSrt/'
            ensure_dir(srtdir)
            srtmerge(listSrt, srtdir + partName + '_new.srt', offset=1000)
            srtToTxt(path+'wholeSrt/')
            """
            srtToTxt(newPath)

def srtToTxt(dirName):
  for infile in glob.glob(os.path.join(dirName, '*.srt')):
    # os.system("iconv --from-code=ISO-8859-1 --to-code=UTF-8 \"" + infile + "\" > \"" + infile2 + "\"")
    #subs = SubRipFile.open(infile)
    try:
      subs = pysrt.open(infile)
    except UnicodeDecodeError:
      subs = pysrt.open(infile,encoding='iso-8859-1')
    outfile = infile[:-4] + '.txt'
    f = codecs.open(outfile, "w", encoding="utf-8")
    #f = open(outfile, 'w')
    for i in range(len(subs)):
      f.write(subs[i].text)
    f.close()

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

if __name__ == '__main__':
  if (len(sys.argv) > 2):
    if sys.argv[1] == "-srt2txt":
      dirName = sys.argv[2]
      srtToTxt(dirName)
    if sys.argv[1] == "-splitMovieAndSrt":
      pathName = sys.argv[2]
      readAllFiles(pathName)
    if sys.argv[1] == "-help":
      print ("- splitMovieAndSrt  -- Read all *.scenes files in a folder and split video and subtitles.\n "
             "                       Argument is a path to a folder with *.scenes files\n")
      print ("- srt2txt           -- Read all *.srt files in a folder and parsing subtitles to txt files.\n "
             "                       Argument is a path to a folder with *.srt files\n")


