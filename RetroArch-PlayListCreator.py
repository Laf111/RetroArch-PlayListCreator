#!/usr/bin/env python3

try:
#----------------------------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------------------------

    import argparse
    import sys
    import pdb
    import os
    from os import listdir
    from os.path import isfile, join
    import time
    import pathlib
    import shutil
    import re

    from tkinter import filedialog
    from tkinter import *


    import concurrent.futures
    from concurrent.futures import ThreadPoolExecutor

    import numpy as np

    import zlib

    import threading

except Exception as e :
    print("Python import failed : %s" %e)
    raise Exception("ERROR")

#----------------------------------------------------------------------------------------------------------
# METHODS
#----------------------------------------------------------------------------------------------------------

def computeCrc32(filePath):
    prev = 0
    for eachLine in open(filePath,"rb"):
        prev = zlib.crc32(eachLine, prev)

    crcStr = "%X"%(prev & 0xFFFFFFFF)
    while len(crcStr) < 8:
        crcStr="0"+crcStr

    return crcStr

def browseToFile():

    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename()

def browseToDir():

    root = Tk()
    root.withdraw()
    return filedialog.askdirectory()

def checkFile(f, relativePath, root):
    global mutex

    mutex.acquire()
    print("Checking "+str(relativePath)+"...")
    mutex.release()

    crc32 = computeCrc32(os.path.join(root, f))



#----------------------------------------------------------------------------------------------------------
# MAIN PROGRAM
#----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    try:
        sys.getwindowsversion()
    except AttributeError:
        isWindows = False
    else:
        isWindows = True
    if isWindows:
        import win32api,win32process,win32con
        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
    else:
        os.nice(-10)

    # define a mutex for working on output files from threads
    mutex = threading.Lock()

    # Pool of os.cpu_count() threads :
    nbThreads = os.cpu_count()

    returnCode = 0
    homeFolder = os.path.dirname(os.path.abspath(__file__))

    # requiered arguments (will be asked if not given)
    parser = argparse.ArgumentParser()
    parser.add_argument("-romsFolderPath", "--Roms_Folder_Path", help = "Folder containing the roms files for the same core", type = str, required = False)
    parser.add_argument("-coreFilePath", "--Core_File_Path", help = "Core file path", type = str, required = False)

    # optional arguments (use default values if not given)
    parser.add_argument("-coreName", "--Core_Name", help = "Core name", type = str, required = False)
    parser.add_argument("-labelDisplayMode", "--Label_Display_Mode", help = "Label Display Mode", type = int, required = False)
    parser.add_argument("-rightThumbnailMode", "--Right_Thumbnail_Mode", help = "Right Thumbnail Mode", type = int, required = False)
    parser.add_argument("-leftThumbnailMode", "--Left_Thumbnail_Mode", help = "Left Thumbnail Mode", type = int, required = False)
    parser.add_argument("-sortMode", "--Sort_Mode", help = "Sort Mode", type = int, required = False)

    # read input parameters
    args = parser.parse_args()
    nbArgs = len(sys.argv)
    if not nbArgs > 1:

        print(" ===================================================")
        print(" usage: RetroArch-PlayListCreator.py\n"+\
              "        [-romsFolderPath ROMS_FOLDER_PATH]\n"+\
              "        [-coreFilePath CORE_FILE_PATH]\n"+\
              "        [-coreName CORE_NAME*]\n"+\
              "        [-labelDisplayMode LABEL_DISPLAY_MODE*]\n"+\
              "        [-rightThumbnailMode RIGHT_THUMBNAIL_MODE*]\n"+\
              "        [-leftThumbnailMode LEFT_THUMBNAIL_MODE*]\n"+\
              "        [-sortMode SORT_MODE*]\n\n"+\
              "        (* for optionals args)")
        print(" ---------------------------------------------------\n"+\
              " return codes:\n"+
              "        0         : OK\n"+\
              "        0<cr<50   : WARNINGS\n"+\
              "        49<cr<100 : ERRORS\n"+\
              "        cr>99     : ARGS ERRORS")
        print(" ===================================================")
        exit(100)

    version="V1-0"
    print("\n -%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
    print("| RetroArch PlayList Creator "+version+" |")
    print(" -%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%-")

    # arg1 : Roms_Folder_Path
    romsFolderPath = args.Roms_Folder_Path
    if romsFolderPath == None:
        pattern = re.compile("^.{1,}$")
        print("Browse on your SDCard to the folder containing roms files...")
        romsFolderPath = os.getcwd()
        folderPicked = ""
        while not pattern.match(folderPicked):
            # open a browse folder dialog
            folderPicked = browseToDir()

            if not folderPicked:
                print("No folder selected, exit with 1")
                exit(1)

        romsFolderPath = folderPicked

    romsFolderPath = str(pathlib.Path(romsFolderPath).resolve())

    # arg2 : Core_File_Path
    coreFilePath = args.Core_File_Path
    pattern = re.compile("^.*[\\]retroarch[\\]cores[\\][a-zA-Z0-9_ -()]{2,}\.rpx$")
    if coreFilePath == None:
        print("Browse to the rpx core file in retroarch/cores...")
        filePicked = ""
        while not pattern.match(filePicked):
            filePicked = browseToFile()

            if not filePicked:
                print("No file selected, exit with 2")
                exit(2)
        coreFilePath = filePicked

    coreFilePath = str(pathlib.Path(coreFilePath).resolve())

    # retroArch path
    retroArchPath = coreFilePath.split("retroarch")[0]+"retroarch"

    # use name of coreFilePathPath as core's name/label
    coreName = (os.path.basename(coreFilePath)).split(".")[0]

    intPattern = re.compile("^[0-9]$")

    if nbArgs > 2:
        labelDisplayMode = args.Label_Display_Mode
        if labelDisplayMode == None:
            while True:
                labelDisplayMode = input("Enter the value of labelDisplayMode (0 to set default)\t: ")
                if intPattern.match(labelDisplayMode):
                    break
        rightThumbnailMode = args.Right_Thumbnail_Mode
        if rightThumbnailMode == None:
            while True:
                rightThumbnailMode = input("Enter the value of rightThumbnailMode (2 to set default): ")
                if intPattern.match(rightThumbnailMode):
                    break
        leftThumbnailMode = args.Left_Thumbnail_Mode
        if leftThumbnailMode == None:
            while True:
                leftThumbnailMode = input("Enter the value of leftThumbnailMode (1 to set default)\t: ")
                if intPattern.match(leftThumbnailMode):
                    break
        sortMode = args.Sort_Mode
        if sortMode == None:
            while True:
                sortMode = input("Enter the value of sortMode (0 to set default)\t\t: ")
                if intPattern.match(sortMode):
                    break
    else:
        # default values
        labelDisplayMode = 0
        rightThumbnailMode = 2
        leftThumbnailMode = 1
        sortMode = 0

    playListFile = os.path.basename(coreFilePath).replace(".rpx", ".lpl")

    print("\n > Create "+playListFile+" for "+retroArchPath+"?\n")

    print(" ===================================================")
    print(" Roms_Folder_Path     = "+romsFolderPath)
    print(" Core_File_Path       = "+coreFilePath)
    print(" Core_Name            = "+coreName)
    print(" Label_Display_Mode   = "+str(labelDisplayMode))
    print(" Right_Thumbnail_Mode = "+str(rightThumbnailMode))
    print(" Left_Thumbnail_Mode  = "+str(leftThumbnailMode))
    print(" Sort_Mode            = "+str(sortMode))
    print(" ===================================================\n")

    pattern = re.compile("^[ynYN]{1}$")
    while True:
        answer = input("Continue (y/n)? : ")
        if pattern.match(answer):
            if answer == "y" or answer == "Y":
                break
            else:
                exit(0)

    print("\n Scanning "+romsFolderPath+"...\n")

    if os.path.exists(playListFile):
        os.remove(playListFile)

    start_time = time.time()
    pattern = re.compile("^\w{1,}\.zip$")

    with open(playListFile, "a") as f:

        # Header :
        header = "{\n"+\
                 "  \"version\": \"1.5\",\n"+\
                 "  \"default_core_path\": \""+"sd:/retroarch/cores/"+coreName+"\",\n"+\
                 "  \"default_core_name\": \""+coreName+"\",\n"+\
                 "  \"label_display_mode\": "+str(labelDisplayMode)+",\n"+\
                 "  \"right_thumbnail_mode\": "+str(rightThumbnailMode)+",\n"+\
                 "  \"left_thumbnail_mode\": "+str(leftThumbnailMode)+",\n"+\
                 "  \"sort_mode\": "+str(sortMode)+",\n"+\
                 "  \"items\": [\n"
        f.write(header)

        nbf = 0
        romsList = []
        for root, subdirectories, files in os.walk(romsFolderPath):
            for rf in sorted(files):
                romName = os.path.basename(rf)
                if pattern.match(romName):
                    romsList.append(os.path.join(romsFolderPath, rf))

        if romsList != None:
            list = sorted(romsList)

            for r in list:
                nbf += 1
                romName = os.path.basename(r)

                crc32 = computeCrc32(r)
                print("> treating "+romName+"...")

                if r != list[-1]:
                    romPart = "    {\n"+\
                              "      \"path\": \"sd:/retroarch"+(r.split("retroarch")[1]).replace("\\","/")+"\",\n"+\
                              "      \"label\": \""+romName.split(".")[0]+"\",\n"+\
                              "      \"core_path\": \"sd:/retroarch/cores/"+coreName+".rpx\",\n"+\
                              "      \"core_name\": \""+str(coreName)+"\",\n"+\
                              "      \"crc32\": \""+str(crc32)+"|crc\",\n"+\
                              "      \"db_name\": \""+str(playListFile)+"\"\n"+\
                              "    },\n"
                else:
                    romPart = "    {\n"+\
                              "      \"path\": \"sd:/retroarch/"+(r.split("retroarch")[1]).replace("\\","/")+"\",\n"+\
                              "      \"label\": \""+romName+"\",\n"+\
                              "      \"core_path\": \"sd:/retroarch/cores/"+coreName+"\",\n"+\
                              "      \"core_name\": \""+str(coreName)+"\",\n"+\
                              "      \"crc32\": \""+str(crc32)+"|crc\",\n"+\
                              "      \"db_name\": \""+str(playListFile)+"\"\n"+\
                              "    }\n"
                f.write(romPart)
        else:
            print("WARNING : No zip files found under "+romsFolderPath)
            returnCode = 3

        end = "  ]\n}\n"
        f.write(end)

        # create folders for thumbnails
        folder = retroArchPath+os.path.sep+"thumbnails"+os.path.sep+playListFile.split(".lpl")[0]+os.path.sep+"Named_Boxarts"

        if not os.path.exists(folder):
            os.makedirs(folder)
        folder = retroArchPath+os.path.sep+"thumbnails"+os.path.sep+playListFile.split(".lpl")[0]+os.path.sep+"Named_Snaps"
        if not os.path.exists(folder):
            os.makedirs(folder)
        folder = retroArchPath+os.path.sep+"thumbnails"+os.path.sep+playListFile.split(".lpl")[0]+os.path.sep+"Named_Titles"
        if not os.path.exists(folder):
            os.makedirs(folder)

    timeStr = "{:.2f}".format(time.time() - start_time)
    print("=====================================================================")
    print(" retroarch"+os.path.sep+"cores"+os.path.sep+"playlist"+os.path.sep+playListFile+" created successfully\n")
    print(" you can move your images to folders in "+os.path.dirname(folder))
    print(" \n"+str(nbf)+" games treated in "+timeStr+" seconds")
    print("=====================================================================")
    if returnCode == 0:
        print("Done successfully")
    else:
        if returnCode > 0 and returnCode < 50:
            print("Done with warnings !")
        else:
            print("Done with errors !!")

    exit(returnCode)
