import os

from mutagen.flac import FLAC, Picture
from mutagen.mp3 import EasyMP3


def tag_flac(filename, root_dir, final_name, d, album, istrack=True, em_image=False):
    """
    Tag a FLAC file

    :param str filename: FLAC file path
    :param str root_dir: Root dir used to get the cover art
    :param str final_name: Final name of the FLAC file (complete path)
    :param dict d: Track dictionary from Qobuz_client
    :param dict album: Album dictionary from Qobuz_client
    :param bool istrack
    :param bool em_image: Embed cover art into file
    """
    audio = FLAC(filename)

    try:
        audio["TITLE"] = "{} ({})".format(d["title"], d["version"])
    except KeyError:
        audio["TITLE"] = d["title"]

    audio["TRACKNUMBER"] = str(d["track_number"])  # TRACK NUMBER

    try:
        audio["WORK"] = d["work"]
    except KeyError:
        pass

    try:
        audio["COMPOSER"] = d["composer"]["name"]  # COMPOSER
    except KeyError:
        pass

    try:
        audio["ARTIST"] = d["performer"]["name"]  # TRACK ARTIST
    except KeyError:
        if istrack:
            audio["ARTIST"] = d["album"]["artist"]["name"]  # TRACK ARTIST
        else:
            audio["ARTIST"] = album["artist"]["name"]

    if istrack:
        audio["GENRE"] = ", ".join(d["album"]["genres_list"])  # GENRE
        audio["ALBUMARTIST"] = d["album"]["artist"]["name"]  # ALBUM ARTIST
        audio["TRACKTOTAL"] = str(d["album"]["tracks_count"])  # TRACK TOTAL
        audio["ALBUM"] = d["album"]["title"]  # ALBUM TITLE
        audio["YEAR"] = d["album"]["release_date_original"].split("-")[0]
    else:
        audio["GENRE"] = ", ".join(album["genres_list"])  # GENRE
        audio["ALBUMARTIST"] = album["artist"]["name"]  # ALBUM ARTIST
        audio["TRACKTOTAL"] = str(album["tracks_count"])  # TRACK TOTAL
        audio["ALBUM"] = album["title"]  # ALBUM TITLE
        audio["YEAR"] = album["release_date_original"].split("-")[0]  # YEAR

    emb_image = os.path.join(root_dir, "cover.jpg")
    if os.path.isfile(emb_image) and em_image:
        try:
            image = Picture()
            image.type = 3
            image.mime = "image/jpeg"
            image.desc = "cover"
            with open(emb_image, "rb") as img:
                image.data = img.read()
            audio.add_picture(image)
        except Exception as e:
            print("Error embedding image: " + str(e))

    audio.save()
    os.rename(filename, final_name)


def tag_mp3(filename, root_dir, final_name, d, album, istrack=True, em_image=False):
    """
    Tag a mp3 file

    :param str filename: mp3 file path
    :param str root_dir: Root dir used to get the cover art
    :param str final_name: Final name of the mp3 file (complete path)
    :param dict d: Track dictionary from Qobuz_client
    :param bool istrack: Embed cover art into file
    :param bool em_image: Embed cover art into file
    """
    # TODO: add embedded cover art support for mp3
    audio = EasyMP3(filename)

    try:
        audio["title"] = "{} ({})".format(d["title"], d["version"])
    except KeyError:
        audio["title"] = d["title"]

    audio["tracknumber"] = str(d["track_number"])

    try:
        audio["discsubtitle"] = d["work"]
    except KeyError:
        pass
    try:
        audio["composer"] = d["composer"]["name"]
    except KeyError:
        pass
    try:
        audio["artist"] = d["performer"]["name"]  # TRACK ARTIST
    except KeyError:
        if istrack:
            audio["artist"] = d["album"]["artist"]["name"]  # TRACK ARTIST
        else:
            audio["artist"] = album["artist"]["name"]

    if istrack:
        audio["genre"] = ", ".join(d["album"]["genres_list"])  # GENRE
        audio["albumartist"] = d["album"]["artist"]["name"]  # ALBUM ARTIST
        audio["album"] = d["album"]["title"]  # ALBUM TITLE
        audio["date"] = d["album"]["release_date_original"].split("-")[0]
    else:
        audio["GENRE"] = ", ".join(album["genres_list"])  # GENRE
        audio["albumartist"] = album["artist"]["name"]  # ALBUM ARTIST
        audio["album"] = album["title"]  # ALBUM TITLE
        audio["date"] = album["release_date_original"].split("-")[0]  # YEAR

    audio.save()
    os.rename(filename, final_name)
