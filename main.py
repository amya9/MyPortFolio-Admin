from flask import Flask , render_template , request , flash , redirect , url_for
import pymongo
from services.mongodb import mongodb_client
import os
import datetime
from werkzeug.utils import secure_filename 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# code for saving files in project directory
UPLOAD_FOLDER_PATH = './data/project-icon'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER_PATH'] = UPLOAD_FOLDER_PATH

db = mongodb_client.db
all_query_collection = db.get_collection("contact")



@app.route('/')
def home_page():
    return render_template("homepage.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add-project' , methods=["GET" , "POST"])
def add_project():
    if request.method == "POST":
        all_project = db.get_collection("projects") 
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(url_for('add_project'))
        project_name = request.form["project_name"]
        project_description = request.form["project_description"]
        project_github_link = request.form["project_github_link"]
        project_live_link = request.form["project_live_link"]
        project_icon = request.files["project_icon"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if project_icon.filename == '':
            flash('No selected file')
            return redirect(url_for('add_project'))
        filename = ""
        print("projectDetail== " , project_name)

        if project_icon and allowed_file(project_icon.filename):
            filename = secure_filename(project_icon.filename)
            project_icon.save(os.path.join(app.config['UPLOAD_FOLDER_PATH'], filename))
            print("filename== ", filename)
            
        projectDetail = {"project_name":project_name , "project_description": project_description , 
                                "project_github_link": project_github_link ,
                                    "project_live_link": project_live_link,
                                        "project_icon_name": filename,
                                        "project_timestamp" : datetime.datetime.utcnow() }
        print("projectDetail== " , projectDetail)

        all_project.insert_one(projectDetail)

    return render_template("addProject.html")

@app.route('/queries')
def all_query():
    #  all_query_json = all_query_collection.find().sort({"_id", pymongo.ASCENDING})
    all_query_json = all_query_collection.find()
    return render_template("query.html" , all_query_json = all_query_json)

if __name__ == "__main__":
    app.run(port=5012 , debug=True )