# RetroArch-PlayListCreator


Simple python script that scan a folder to get roms (expected as zip files), compute the CRC32 and create the RetroArch playlist (in retroarch/cores/playplist) and Thumbnails folder structure.


Require python 3, Tk, numpy imports


## usage: **RetroArch-PlayListCreator.py**

[-romsFolderPath ROMS_FOLDER_PATH]

[-coreFilePath CORE_FILE_PATH]

[-coreName CORE_NAME*]

[-labelDisplayMode LABEL_DISPLAY_MODE*]

[-rightThumbnailMode RIGHT_THUMBNAIL_MODE*]

[-leftThumbnailMode LEFT_THUMBNAIL_MODE*]

[-sortMode SORT_MODE*]


(* for optionals args)


## return codes:

0         : OK

0<cr<50   : WARNINGS

49<cr<100 : ERRORS

cr>99     : ARGS ERRORS
 
