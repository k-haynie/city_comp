from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from queryMaster import queryState
import requests
import os

# configures the app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# establishes variables
states = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','AS','GU','MP','PR','VI']
fips = ['01','02','04','05','06','08','09','10','11','12','13','15','16','17','18','19','20','21','22', '23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','44','45','46','47','48','49','50','51','53','54','55','56','72']
options = 2

# establishes API keys
gov_api = os.environ.get("fbi_api")
cov_api = os.environ.get("covid_api")
census_api = os.environ.get("census_api")


@app.route("/back", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    global options
    if request.method == "GET":
        return render_template("index.html", states=states, options=options)
    elif request.method == "POST":
        queries = []
        for i in range(options):
            state = request.form.get(f"state{i}")
            city = request.form.get(f"city{i}")
            if city != '':
                queries.append([city, state])


        if request.form.get("Add") == "Add":
            if options <= 5:
                options += 1
            return render_template("index.html", states=states, options=options, queries=queries)
        elif request.form.get("Subtract") == "Subtract":
            if options > 2:
                options -= 1
            return render_template("index.html", states=states, options=options, queries=queries)
        else:
            if len(queries) == 0:
                return render_template("index.html", states=states, options=options)

            returned = []
            for x in queries:
                info = queryState(x[0], x[1], states, fips, gov_api, cov_api, census_api).get_answer()
                returned.append(info)

            return render_template("results.html", returned=returned, cityState=queries)

@app.route("/about")
def about():
    return render_template("about.html")