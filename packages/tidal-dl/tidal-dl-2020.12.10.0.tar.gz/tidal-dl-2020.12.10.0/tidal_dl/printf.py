#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   printf.py
@Time    :   2020/08/16
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import prettytable
from aigpy.cmdHelper import red, green, blue, yellow, TextColor, myprint
from tidal_dl.lang.language import getLangName, getLang
from tidal_dl.settings import Settings, getSettingsPath
from tidal_dl.model import Album, Track, Video, Playlist, Artist

__LOGO__ = '''
 /$$$$$$$$ /$$       /$$           /$$               /$$ /$$
|__  $$__/|__/      | $$          | $$              | $$| $$
   | $$    /$$  /$$$$$$$  /$$$$$$ | $$          /$$$$$$$| $$
   | $$   | $$ /$$__  $$ |____  $$| $$ /$$$$$$ /$$__  $$| $$
   | $$   | $$| $$  | $$  /$$$$$$$| $$|______/| $$  | $$| $$
   | $$   | $$| $$  | $$ /$$__  $$| $$        | $$  | $$| $$
   | $$   | $$|  $$$$$$$|  $$$$$$$| $$        |  $$$$$$$| $$
   |__/   |__/ \_______/ \_______/|__/         \_______/|__/
   
       https://github.com/yaronzz/Tidal-Media-Downloader 
'''
VERSION = '2020.12.10.0'

class Printf(object):

    @staticmethod
    def logo():
        print(__LOGO__)
        print('                      v' + VERSION)

    @staticmethod
    def usage():
        print("=============TIDAL-DL HELP==============")
        tb = prettytable.PrettyTable()
        tb.field_names = [green("OPTION"), green("DESC")]
        tb.align = 'l'
        tb.add_row(["-h or --help", "show help-message"])
        tb.add_row(["-v or --version", "show version"])
        tb.add_row(["-o or --output", "download path"])
        tb.add_row(["-l or --link", "url/id/filePath"])
        tb.add_row(["-q or --quality", "track quality('Normal','High,'HiFi','Master')"])
        tb.add_row(["-r or --resolution", "video resolution('P1080', 'P720', 'P480', 'P360')"])
        #tb.add_row(["-u or --username", "account-email"])
        #tb.add_row(["-p or --password", "account-password"])
        #tb.add_row(["-a or --accessToken", "account-accessToken"])
        print(tb)

    @staticmethod
    def settings(data:Settings):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [green(LANG.SETTING), green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row(["Settings path", getSettingsPath()])
        tb.add_row([LANG.SETTING_DOWNLOAD_PATH, data.downloadPath])
        tb.add_row([LANG.SETTING_ONLY_M4A, data.onlyM4a])
        # tb.add_row([LANG.SETTING_ADD_EXPLICIT_TAG, data.addExplicitTag])
        # tb.add_row([LANG.SETTING_ADD_HYPHEN, data.addHyphen])
        # tb.add_row([LANG.SETTING_ADD_YEAR, data.addYear])
        # tb.add_row([LANG.SETTING_USE_TRACK_NUM, data.useTrackNumber])
        tb.add_row([LANG.SETTING_AUDIO_QUALITY, data.audioQuality])
        tb.add_row([LANG.SETTING_VIDEO_QUALITY, data.videoQuality])
        tb.add_row([LANG.SETTING_CHECK_EXIST, data.checkExist])
        tb.add_row([LANG.SETTING_SHOW_PROGRESS, data.showProgress])
        # tb.add_row([LANG.SETTING_ARTIST_BEFORE_TITLE, data.artistBeforeTitle])
        # tb.add_row([LANG.SETTING_ALBUMID_BEFORE_FOLDER, data.addAlbumIDBeforeFolder])
        tb.add_row([LANG.SETTING_INCLUDE_EP, data.includeEP])
        tb.add_row([LANG.SETTING_SAVE_COVERS, data.saveCovers])
        tb.add_row([LANG.SETTING_LANGUAGE, getLangName(data.language)])
        tb.add_row([LANG.SETTING_USE_PLAYLIST_FOLDER, data.usePlaylistFolder])
        tb.add_row([LANG.SETTING_MULITHREAD_DOWNLOAD, data.multiThreadDownload])
        tb.add_row([LANG.SETTING_ALBUM_FOLDER_FORMAT, data.albumFolderFormat])
        tb.add_row([LANG.SETTING_TRACK_FILE_FORMAT, data.trackFileFormat])
        print(tb)

    @staticmethod
    def choices():
        LANG = getLang()
        print("====================================================")
        tb = prettytable.PrettyTable()
        tb.field_names = [LANG.CHOICE, LANG.FUNCTION]
        tb.align = 'l'
        tb.set_style(prettytable.PLAIN_COLUMNS)
        tb.add_row([green(LANG.CHOICE_ENTER + " '0':"), LANG.CHOICE_EXIT])
        tb.add_row([green(LANG.CHOICE_ENTER + " '1':"), LANG.CHOICE_LOGIN])
        tb.add_row([green(LANG.CHOICE_ENTER + " '2':"), LANG.CHOICE_SETTINGS])
        tb.add_row([green(LANG.CHOICE_ENTER + " '3':"), LANG.CHOICE_LOGOUT])
        tb.add_row([green(LANG.CHOICE_ENTER + " '4':"), LANG.CHOICE_SET_ACCESS_TOKEN])
        tb.add_row([green(LANG.CHOICE_ENTER_URLID), LANG.CHOICE_DOWNLOAD_BY_URL])
        print(tb)
        print("====================================================")

    @staticmethod
    def enter(string):
        myprint(string, TextColor.Yellow, None)
        ret = input("")
        return ret

    @staticmethod
    def err(string):
        LANG = getLang()
        print(red(LANG.PRINT_ERR + " ") + string)
    
    @staticmethod
    def info(string):
        LANG = getLang()
        print(blue(LANG.PRINT_INFO + " ") + string)

    @staticmethod
    def success(string):
        LANG = getLang()
        print(green(LANG.PRINT_SUCCESS + " ") + string)

    @staticmethod
    def album(data: Album):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [green(LANG.MODEL_ALBUM_PROPERTY), green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.title])
        tb.add_row(["ID", data.id])
        tb.add_row([LANG.MODEL_TRACK_NUMBER, data.numberOfTracks])
        tb.add_row([LANG.MODEL_VIDEO_NUMBER, data.numberOfVideos])
        tb.add_row([LANG.MODEL_RELEASE_DATE, data.releaseDate])
        tb.add_row([LANG.MODEL_VERSION, data.version])
        tb.add_row([LANG.MODEL_EXPLICIT, data.explicit])
        print(tb)

    @staticmethod
    def track(data:Track):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [green(LANG.MODEL_TRACK_PROPERTY), green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.title])
        tb.add_row(["ID", data.id])
        tb.add_row([LANG.MODEL_ALBUM, data.album.title])
        tb.add_row([LANG.MODEL_VERSION, data.version])
        tb.add_row([LANG.MODEL_EXPLICIT, data.explicit])
        print(tb)
    
    @staticmethod
    def video(data):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [green(LANG.MODEL_VIDEO_PROPERTY), green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.title])
        tb.add_row([LANG.MODEL_ALBUM, data.album.title if data.album != None else None])
        tb.add_row([LANG.MODEL_VERSION, data.version])
        tb.add_row([LANG.MODEL_EXPLICIT, data.explicit])
        print(tb)

    @staticmethod
    def artist(data:Artist, num):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [green(LANG.MODEL_ARTIST_PROPERTY), green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_ID, data.id])
        tb.add_row([LANG.MODEL_NAME, data.name])
        tb.add_row(["Number of albums", num])
        tb.add_row([LANG.MODEL_TYPE, str(data.type)])
        print(tb)

    @staticmethod
    def playlist(data):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [green(LANG.MODEL_PLAYLIST_PROPERTY), green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.title])
        tb.add_row([LANG.MODEL_TRACK_NUMBER, data.numberOfTracks])
        tb.add_row([LANG.MODEL_VIDEO_NUMBER, data.numberOfVideos])
        print(tb)

