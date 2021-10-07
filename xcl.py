import json
import csv, sys

def convert(data_json, output="output.json"):
    if type(data_json)== str:
        with open(data_json, "r") as file:
            data = json.load(file)

    header = ["Document Name", "Coordinate Location"]
    with open(output, 'w') as csv_file:  
        writer = csv.writer(csv_file)

        writer.writerow(header)
        for key, value in data.items():
            if not value:
                writer.writerow([key, value])
            for i in value:
                writer.writerow([key, i])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Provide the argument for json file with coordinates. Eg; python xcl.py data.json")
    else:
        convert(sys.argv[1])


