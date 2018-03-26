import dlib, face_recognition, os
from PIL import ImageTk, Image
import psycopg2

"""
The following file does the same thing as the GUI app version but is
stripped down to just a command line interface.

Command line:
$ python3 load_db.py <filename *.jpg *.png> <firstname> <lastname>

* note
easy way is to just have file in current directory
"""

filename = sys.argv[1]
firstname = sys.argv[2]
lastname = sys.argv[3]

image = face_recognition.load_image_file(filename)
face_encoding = face_recognition.face_encodings(image)[0] #only 1 face expected when entering 'mugshot'
face_encoding_string = "("

for distance in face_encoding:
    face_encoding_string+=str(distance)
    face_encoding_string+=str(",")

face_encoding_string = face_encoding_string[:-1]
face_encoding_string += str(")")

print(face_encoding_string) # demo what a face encoding data looks like in the output

conn = psycopg2.connect(host="localhost",database="postgres", user="postgres", password="password")
cur = conn.cursor()
cur.execute("INSERT INTO wanted (first_name, last_name, face_encoding) VALUES ('"+firstname+"', '"+lastname+"', '"+face_encoding_string+"')");
conn.commit()
conn.close()
self.SetDefault()
