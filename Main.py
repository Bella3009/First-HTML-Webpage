from flask import Flask,render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME"]]
@app.route("/")
def home():
	return render_template("Weather_index.html", place=stations.to_html())
	
@app.route("/api/v1/<station>/<date>")
def dt(station, date):
    
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    
    data = pd.read_csv(filename, skiprows = 20, parse_dates=["    DATES"])
    temperature = data.loc[data["    DATE"] == date] ["    TG"].squeeze()/10
    
    return {"station": station,
                 "date": date,
                 "temperature": temperature}
@app.route("/api/v1/<station>")
def statonly(station):
    
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    data = pd.read_csv(filename, skiprows = 20, parse_dates=["    DATES"])
    result = data.to_dict(orient="records")
    return result
	
@app.route("/api/v1/yearly/<station>/<year>")
def dt(station, year):
    
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    data = pd.read_csv(filename, skiprows = 20)
    data["    DATES"] = data["    DATES"].astype(str)
    result = data[data["    DATES"].str.startswith(str(year))]
    return result

if __name__ == "__main__":
    app.run(debug=True)
