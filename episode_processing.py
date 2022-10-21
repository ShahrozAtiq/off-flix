import cv2
from pymediainfo import MediaInfo
import hashlib
import os
import subprocess
from db import get_con

def convert_ms(millis):
    millis = int(millis)
    seconds=(millis/1000)%60
    seconds = str(int(seconds))
    minutes=(millis/(1000*60))%60
    minutes = str(int(minutes))
    hours=str(int((millis/(1000*60*60))%24))
    hours = "0"+hours if len(hours) < 2 else hours
    minutes = "0"+minutes if len(minutes) < 2 else minutes
    seconds = "0"+seconds if len(seconds) < 2 else seconds

    return "{}:{}:{}".format(hours, minutes, seconds)
    
def get_duration(file):
    media_info = MediaInfo.parse(file)
    duration_in_ms = media_info.tracks[0].duration
    return duration_in_ms
def get_thumbnail_name(file):
    hash = hashlib.sha256(file.encode())
    filename = hash.hexdigest() + ".jpg"#os.path.splitext(file)[-1]
    return filename

# def get_thumbnail(file, save):
#     cap= cv2.VideoCapture(file)
#     length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     ss_frame = int(length * 0.02)
#     ss_frame = 250 if ss_frame > 250 else ss_frame
#     i=0
#     for i in range(ss_frame):
#         ret, frame = cap.read()
#         if ret == False:
#             break
    
#     thumb_title = get_thumbnail_name(file)
#     path = os.path.join(save, thumb_title)

#     cv2.imwrite(path ,frame)
    
#     cap.release()
#     cv2.destroyAllWindows()
#     return path

def get_thumbnail(file):
    save = r'static\images\thumbnails'
    thumb_name = get_thumbnail_name(file)
    output = os.path.join(save, thumb_name)
    duration = get_duration(file)
    thumb_time = 7
    thumb_time = thumb_time if duration > thumb_time else (duration//2 )//1000
    cmd = f'ffmpeg -i "{file}" -ss {thumb_time} -vframes 1 "{output}" -y'.replace('\\', '/')
    subprocess.call(cmd)
    return thumb_name

def get_ep_data(season, part):
    con = get_con()
    
    with con:
        sql = f"SELECT id, title, watched, thumbnail, duration FROM episodes where season = {season} AND part = {part}"
        data = con.execute(sql)
        data = data.fetchall()
    columns = ['id', 'title', 'watched', 'thumbnail', 'duration']
    data = [dict(zip(columns, i)) for i in data]
    return data

def add_to_watched(id):
    con = get_con()
    with con:
        sql = f'UPDATE episodes SET watched = 1  WHERE id = {id};'
        con.execute(sql)   
        
def get_ep_path(id):
    con = get_con()
    with con:
        sql = f"SELECT path FROM episodes WHERE id= {id}"
        ep = con.execute(sql)
        ep = ep.fetchone()[0]
    return ep

if __name__ == "__main__":
    print(get_thumbnail(r"C:\Users\shoai\Downloads\Compressed\Halt and Catch Fire Season 1 COMPLETE S01 720p HDTV x264 [MKV,AC3,5.1] Ehhhh\S01E06 - Landfall - Ehhhh.mkv",
                    r"D:\Documents\1. Python\Off-flix"))