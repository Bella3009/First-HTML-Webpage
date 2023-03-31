from flask import Flask,render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("Weather_index.html")
	
@app.route("/api/v1/<station>/<date>")
def dt(station, date):
    
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    
    data = pd.read_csv(filename, skiprows = 20, parse_dates=["    DATES"])
    temperature = data.loc[data["    DATE"] == date] ["    TG"].squeeze()/10
    
    return {"station": station,
                 "date": date,
                 "temperature": temperature}
if __name__ == "__main__":
    app.run(debug=True)
