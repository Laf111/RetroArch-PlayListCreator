# RetroArch-PlayListCreator


Simple python script that scans a folder to get roms (expected as zip files), compute the CRC32 and create the RetroArch playlist v1.5 (in retroarch/cores/playlist) and thumbnails folder structure.


Require python 3, Tk, numpy imports


## usage: 

You call call the script without args or use the following syntax (you can pass the number of those args you want)


**RetroArch-PlayListCreator.py**

[-romsFolderPath ROMS_FOLDER_PATH]

[-coreFilePath CORE_FILE_PATH]

[-coreName CORE_NAME]

[-labelDisplayMode LABEL_DISPLAY_MODE]

[-rightThumbnailMode RIGHT_THUMBNAIL_MODE]

[-leftThumbnailMode LEFT_THUMBNAIL_MODE]

[-sortMode SORT_MODE]


For example : RetroArch-PlayListCreator.py -romsFolderPath "D:\retroarch\Downloads\roms\MAME"


## return codes:

0         : OK

0<cr<50   : WARNINGS

49<cr<100 : ERRORS

cr>99     : ARGS ERRORS
 

## sample of playlist file generated : 
![image](https://user-images.githubusercontent.com/47532310/158772723-1ba18275-2907-48f5-ac83-72da8bfe5fe6.png)
