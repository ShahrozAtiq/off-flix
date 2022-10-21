from db import get_con
import os
import mimetypes
import episode_processing
import random 
from shutil import copyfile


def is_video(file):
    try:
        return mimetypes.guess_type(file)[0].startswith('video')
    except:
        return False

def get_all_episodes(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_all_episodes(fullPath)
        else:
            allFiles.append(fullPath)

    allFiles = [ep for ep in allFiles if is_video(ep)]
                
    return allFiles

def get_season_title(id):
    con = get_con()
    with con:
        sql = f"SELECT title FROM seasons WHERE id = {id}"
        season = con.execute(sql)
        season = season.fetchone()[0]
    return season

def get_parts(id):
    con = get_con()
    with con:
        sql = f"SELECT id, title FROM parts WHERE season = {id}"
        parts = con.execute(sql)
        parts = parts.fetchall()
    parts = [dict(zip(['id', 'title'], part)) for part in parts]
    return parts

def add_season(path):
    path = os.path.realpath(path)
    title = os.path.split(path)[-1]
    poster = get_poster(path)
    poster = "default.jpg" if not poster else poster
    con = get_con()
    sql = 'INSERT INTO seasons (title, path, poster) values(?, ?, ?)'
    data = [
        (title, path, poster)
    ]

    with con:
        con.executemany(sql, data)
        dat = con.execute("SELECT id FROM seasons ORDER BY id DESC LIMIT 1")
        last_row_id = dat.fetchone()[0]
    add_parts(path, last_row_id)
    add_episodes(path, last_row_id)
    

def add_episodes(path, season_id):
    path = os.path.realpath(path)
    episodes = get_all_episodes(path)
    values = []
    for path in episodes:
        title = os.path.split(path)[-1]
        title =os.path.splitext(title)[0]
        watched = 0
        duration = episode_processing.get_duration(path)
        duration = str(int((duration/1000) / 60)) + 'm'
        thumbnail = episode_processing.get_thumbnail(path)
        con = get_con()
        with con:
            part_path = os.path.split(path)[0]
            sql = f"SELECT id FROM parts WHERE path = '{part_path}' ORDER BY id DESC LIMIT 1"
            print(sql)
            part = con.execute(sql)
            part = part.fetchone()[0]

        values.append((path, title, watched, thumbnail, duration, season_id, part))
    sql = 'INSERT INTO episodes (path, title, watched, thumbnail, duration, season, part) values(?, ?, ?, ?, ?, ?, ?)'
    con = get_con()
    with con:
        con.executemany(sql, values)

def add_parts(path, season_id):
    path = os.path.realpath(path)
    sub_paths = [f.path for f in os.scandir(path) if f.is_dir()]
    sub_titles = [os.path.split(folder)[-1] for folder in sub_paths]
    values = list(zip(sub_paths, sub_titles, [season_id]*len(sub_paths)))
    sql = 'INSERT INTO parts (path, title, season) values(?, ?, ?)'
    con = get_con()
    with con:
        con.executemany(sql, values)


def get_poster(path):
    files = [os.path.join(path, file) for file in os.listdir(path)]
    files = [file for file in files if os.path.isfile(file)]
    files = [file for file in files if os.path.split(file)[-1].lower().startswith('poster.')]
    if files != []:
        poster = files[0]
        poster_name = episode_processing.get_thumbnail_name(poster)
        dest = os.path.join("static/images/posters/", poster_name)
        copyfile(poster, dest)
        return poster_name

def get_seasons_data():
    con = get_con()
    with con:
        sql = f'SELECT * from seasons ORDER BY id DESC;'
        data = con.execute(sql)
        data = data.fetchall()
    columns = ("id", "title", "path", "current_part", "poster")
    data = [dict(zip(columns, i)) for i in data]
    return data

def get_first_part(season):
    con = get_con()
    with con:
        sql = f"SELECT id FROM parts WHERE season = {season} ORDER BY path LIMIT 1"
        data = con.execute(sql)
        part = data.fetchone()[0]
    return part

def delete_show(id):
    con = get_con()
    with con:
        sql = f"""DELETE FROM episodes WHERE season = {id};
        DELETE FROM parts WHERE season = {id};
        DELETE FROM seasons WHERE id = {id};"""
        con.executescript(sql)
def play_random(season_id):
    con = get_con()
    with con:
        sql = f"SELECT path FROM episodes WHERE season = {season_id};"
        data = con.execute(sql)
        episodes = data.fetchall()
    random_ep = random.choice(episodes)[0]
    os.startfile(random_ep)

def set_current_part(season_id, part):
    con = get_con()
    with con:
        sql = f"UPDATE seasons SET current_part = {part}  WHERE id = {season_id};"
        con.execute(sql)
def get_current_part(season_id):
    con = get_con()
    with con:
        sql = f"SELECT current_part FROM seasons WHERE id = {season_id};"
        data = con.execute(sql)
        part = data.fetchone()[0]
    return part

from db import get_con
def season_exists(path):
    path = os.path.realpath(path)
    con = get_con()
    with con:
        sql = f"SELECT * from seasons WHERE path = '{path}';"
        data = con.execute(sql)
        data = data.fetchone()
    return data is not None

if __name__ == '__main__':
    add_season(r"D:\Seasons\FRIENDS")
    add_season(r"D:\Seasons\The Office")
    add_season(r"D:\Seasons\The Queens Gambit")
    add_season(r"D:\Seasons\The Sinner")
    add_season(r"D:\Seasons\True Detective")
    add_season(r"D:\Seasons\WandaVision")
    add_season(r"D:\Seasons\The Falcon and The Winter Solider")

