1) Open terminal/command prompt in project directory where the python libraries exist
2) Install libraries using : pip install -r requirements.txt
3) Run command : python app.py <output_file_name> (eg; python app.py data.json)
4) Open http://localhost:5000 on browser and upload files

NOTE:
When running locally on windows, the poppler path must be provided as an argument to convert_from_path() like so : convert_from_path(path, poppler_path=r"C:\poppler-0.68.0\bin")

Currently the application is hosted at : https://error-detection.herokuapp.com/




