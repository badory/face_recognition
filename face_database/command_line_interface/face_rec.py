from PIL import Image, ImageDraw
from PIL import ImageTk, Image
import os, numpy, scipy, dlib, face_recognition, psycopg2, sys

"""
* The following file does the same thing as the GUI app version but is
stripped down to just a command line interface.
* Intead of showing results in GUI, distance results and all names
found in the image are printed to console

Command Line:
$ python3 face_rec.py <filename *.jpg *.png>

* note:
easy way is to just have file in current directory
"""

THRESHOLD = 0.6 # threshold, declare that 2 faces are not a close enough match

filename = sys.argv[1]

#connect db
conn = psycopg2.connect(host="localhost",database="postgres", user="postgres", password="password")
cur = conn.cursor()

image = face_recognition.load_image_file(filename)
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

#all responses stored in list
response_list = []

# loops through all detected faces and query db for closest match face encoding
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

    # build face encoding query
    face_encoding_string = ""
    for float_distance in face_encoding:
        face_encoding_string += str(float_distance)
        face_encoding_string += str(",")
    face_encoding_string = face_encoding_string[:-1]
    # finished building face encoding query
    # now query the database search for closest match face encoding (spatial geometry database query)
    query = "SELECT first_name, last_name, face_encoding FROM wanted ORDER BY face_encoding <-> cube(array["+face_encoding_string+"]) LIMIT 1"
    cur.execute(query) #execute query
    response = cur.fetchone()
    response = [response[0], response[1],response[2]]

    # need to check a threshold here to see if its even close enough...
    # need to compare face_ending with response[2] (face_ending from db)
    returned_face_encoding = response[2] # array of returned face encodings
    returned_face_encoding = returned_face_encoding.replace("(","")
    returned_face_encoding = returned_face_encoding.replace(")","")
    returned_face_encoding = [float(x) for x in returned_face_encoding.split(",")]

    A = numpy.array(face_encoding)
    B = numpy.array(returned_face_encoding)
    distance = scipy.spatial.distance.euclidean(A, B)
    print(distance)

    if distance > THRESHOLD:
        response[0] = "Unknown"
        response[1] = "Unknown"

    response_list.append(response)
#end for loop

conn.close() #close database connection

printallnames = ""
for response in response_list:
    printallnames += response[0] + " " + response[1] + "\n"

print(printallnames)
