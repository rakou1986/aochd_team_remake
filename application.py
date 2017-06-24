#coding: utf-8

from flask import Flask, request, render_template
from utils import team_assign
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def team_remake():
  if request.method == "POST":
    remaked = team_assign(request.form["aochd_team_str"])
    return render_template(
      "team_remake.html",
      aochd_team_str=request.form["aochd_team_str"],
      remaked=remaked
      )
  return render_template("team_remake.html")
