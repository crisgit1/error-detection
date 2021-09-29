import os
import sys
import cv2
import glob
import json
import imutils  
import numpy as np
from pathlib import Path 
from pdf2image import convert_from_path

_tmp, _format = "tmp.png", "PNG"

def extract_sheet_number(path):
    p = Path(path).stem
    print("Extracting sheet number " + p)
    return p
    
def safe_delete(img_png):
    
    if os.path.exists(img_png):
        os.remove(img_png)   

def convert_to_png(path):
    print("Converting to png " + path)
    image = convert_from_path(path)
    for img_png in image:
        img_png.save(_tmp, _format)
        lst_coordinates = extract_shapes(_tmp)
        safe_delete(_tmp)

    return lst_coordinates

def extract_shapes(path):
    print("Extracting shapes from " + path)
    image = cv2.imread(path)
    original = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 200, 100])
    upper = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(original,original,mask=mask)
    result[mask<=50] = (255,255,255)

    # Make text black and foreground white
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    result = cv2.threshold(result, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    cv2.imwrite(_tmp, result)
    image = cv2.imread(_tmp)

    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    shapeMask = cv2.inRange(image, lower, upper)
    cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
       
    # loop over the contours
    lst=[]
    for c in cnts:
        # draw the contour and show it
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0,0), 20)
        center = (x,y)
        lst.append(center)
        

    cv2.imwrite(_tmp, image)
    return lst

def main(folder_path, output_file):
    filespath = glob.glob(os.path.join(folder_path, "**", "*.pdf"), recursive = True)
    dct = {}
    for files in filespath:
        dct.update({extract_sheet_number(files): convert_to_png(files)})
    with open(output_file, "w") as file:
        json.dump(dct, file, indent=2)
    return dct 

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide the <folder_path> and <output_json_file_name> arguments as input. eg; python extract.py pdfs/ data.json")
    else:
        try:
            main(sys.argv[1], sys.argv[2])
        except Exception as e:
            print("There was problem extracting coordinates. [ERROR] {}".format(e))
    


