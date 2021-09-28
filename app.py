from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import extract
import json
import os, glob
import sys

app = Flask(__name__)

try:
   data_json = sys.argv[1]
except:
   data_json = "data.json"

script_file_name = "app.py"

@app.route('/')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files.getlist("file")
      print(f)
      for f1 in f: f1.save(secure_filename( f1.filename))
      
      full_path = os.path.realpath(script_file_name)
      real_path, _ = os.path.split(full_path) 
      
      data = extract.main(real_path, data_json)
    
      with open(data_json, "w") as file:
          json.dump(data, file, indent=2)
      
      # Deleting pdfs
      filespath = glob.glob(os.path.join(real_path, "**", "*.pdf"), recursive = True)
      for files in filespath:
         extract.safe_delete(files)

      try:
         return send_file(data_json, attachment_filename='data.json',  as_attachment=True)
      except Exception as e:
         return str(e)



   

if __name__ == '__main__':
   app.run(debug = True, port=33507)
   
   