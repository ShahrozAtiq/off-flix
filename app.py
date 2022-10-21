from flask import Flask, render_template, request, make_response, redirect
import os
import episode_processing, season_processing
from urllib.parse import unquote
import subprocess

app = Flask(__name__)

@app.route('/',)
def index():
    data = season_processing.get_seasons_data()
    return render_template("index.html", seasons = data)

@app.route('/season/<season>/',)
def season(season):
    _part = season_processing.get_current_part(season)
    if _part is None:
        _part = season_processing.get_first_part(season)
    return redirect(f'/season/{season}/{_part}')


@app.route('/season/<season>/<part>',)
def part(season, part):
    data = episode_processing.get_ep_data(season, part)
    season_title = season_processing.get_season_title(season)
    parts = season_processing.get_parts(season)
    season_processing.set_current_part(season, part)
    return render_template("episodes.html", episodes = data,
                             season_title = season_title, parts = parts)

@app.route("/add/<path>")
def add(path):
    print("Adding new season")
 
    season_processing.add_season(path)
    return redirect("/")
@app.route("/delete/<id>")
def delete(id):
    season_processing.delete_show(int(id))
    return redirect("/")

@app.route('/play/<id>',)
def play(id):
    id = int(id)
    ep = episode_processing.get_ep_path(id)
    episode_processing.add_to_watched(id)
    os.startfile(ep)
    return {} 

@app.route("/random/<season_id>")
def play_random(season_id):
    season_id = int(season_id)
    season_processing.play_random(season_id)
    return {}

if __name__ == "__main__":
    app.run(debug=True)
    
