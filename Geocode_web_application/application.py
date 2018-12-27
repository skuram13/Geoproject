from flask import Flask, render_template, request,send_file
from geopy.geocoders import ArcGIS
import pandas as pd
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db_string = 'postgres://tazoxgldowebdu:d1676ea6a1add2937b87f7024a7a1adbd8634f18c618b7e964a3f6f9154b67ad@ec2-54-235-178-189.compute-1.amazonaws.com:5432/d1fv92bu0oqtcr?sslmode=require'
db_engine = create_engine(db_string)

app = Flask(__name__)



# Setting the configuration of the flask app about the sqlalchemy i.e. the database we are attempting
# to connect using to connect for this web application
app.config['SQLALCHEMY_DATABASE_URI']='postgres://tazoxgldowebdu:d1676ea6a1add2937b87f7024a7a1adbd8634f18c618b7e964a3f6f9154b67ad@ec2-54-235-178-189.compute-1.amazonaws.com:5432/d1fv92bu0oqtcr?sslmode=require'
# 'postgresql://postgres:postgres@localhost/geocode_db'
# creating a database object of sqlalchemy so that the web app can directly talk to the database
# which is postgres in our case but it can be any database
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submitFile",methods=["POST"])
def submitFile():
    global filename
    global data
    file = request.files['upload_file']
    try:
        data = pd.read_csv(file, index_col=False)
        print("After read_Csv")
        gc = ArcGIS(scheme='http')
        data["coordinates"] = data["Address"].apply(gc.geocode)
        data['Latitude'] = data['coordinates'].apply(lambda x: x.latitude if x != None else None)
        data['Longitude'] = data['coordinates'].apply(lambda x: x.longitude if x != None else None)
        data = data.drop("coordinates", 1)
        filename = datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
        data.to_csv(filename, index=False)
        print("After To_Csv")
        print(data)
        return render_template("index.html", text=data.to_html(), btn='download.html')
    except Exception as e:
        return render_template("index.html", text=str(e))

@app.route("/download-file")
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        print(data)
        data.to_sql(name='geocoder_tbl', con=db_engine, if_exists='replace')
        return render_template("success.html")

    return render_template("index.html", text="Seems like something went wrong")

if __name__=='__main__':
    app.debug=True
    app.run()
