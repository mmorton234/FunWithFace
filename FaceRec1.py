import face_recognition
import cv2
import os
import getpass
import time
import glob



# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

########
save = 'D:/Hack2018/Test3'
#SavedPics = (glob.glob("D:/hack2018/test1\*.jpg"))
#for 
    
#print (SavedPics[0])

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
#Matt_image = face_recognition.load_image_file("Matt.jpg")
#Matt_face_encoding = face_recognition.face_encodings(Matt_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    []
]
known_face_names = [
    
]
#looks a files and picks out jpg phots and enters them as people into the system print
SavedPics = (glob.glob("D:/hack2018/test3\*.jpg"))
print (SavedPics)
i=0
def Locate_Name(Name):
    ji =0
    while ji<len(known_face_names):
        if (Name==known_face_names[ji]):
            return ji
        ji+=1
    return -1

def Encode_Image(image, name):
    Temp_image = face_recognition.load_image_file(image)

    if (0<(len(face_recognition.face_locations(Temp_image)))):
        face_encoding = face_recognition.face_encodings(Temp_image)[0]
        face_id=Locate_Name(name)
        if (face_id==-1):
            known_face_names.append(name)
            known_face_encodings.append([])
        
        face_id=Locate_Name(name)
        known_face_encodings[face_id].append(face_encoding)
    else:
        os.remove(image)


    
while i<len(SavedPics):
    print (str(i))
    SavedPics[i]=SavedPics[i].replace('D:/hack2018/test3\\','')
    SavedPics[i]=SavedPics[i].replace('.jpg','')
    print (SavedPics[i])
    Encode_Image(str(SavedPics[i]+'.jpg'), SavedPics[i])
    print("known faces "+str(i+1)+" "+SavedPics[i])
    i+=1
    #Temp_image = face_recognition.load_image_file(SavedPics[i])
    #Temp_face_encoding = face_recognition.face_encodings(Temp_image)[0]
    #known_face_encodings.append(Temp_face_encoding)
    
    #know_face_compare = Locate_Name(SavedPics[i])
    #if (know_face_compare==-1):
     #   known_face_names.append(SavedPics[i])
     #   known_face_encodings.append(Temp_face_encoding[len(known_face_encodings)])
    #else:
     #   known_face_encodings.append(Temp_face_encoding[know_face_compare])

    

   
    #SavedPics[i]=SavedPics[i].replace('.jpg','')
    

unknown_counter = 0


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        
        for face_encoding in face_encodings:
            w=0
            while (w<len(known_face_encodings)):

                #print(w)
                #print (face +"     --   "+ppprint (str(len(face_encodings[w])))
            # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings[w], face_encoding)
                name = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[w]
                    print(w)
                    break
                w+=1
                
            face_names.append(name)
            
                


    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        #to find new face crop it and store it 
        if (name == "Unknown" and (0<(len(face_recognition.face_locations(frame))))):
            print(name)
            crop_img = frame[int(top):int(bottom),int(left):int(right)]
            if (0<(len(face_recognition.face_locations(crop_img)))):
                temp_name= ("Unknown"+str(i))
                cv2.imwrite(os.path.join(save, (temp_name+".jpg")), crop_img)
                Encode_Image((temp_name+".jpg"),temp_name) 

            #Face_id = (face_recognition.face_encodings(face_recognition.load_image_file(temp_name+".jpg"))[0])
            #known_face_names.append(temp_name)
            #know_face_compare = Locate_Name(temp_name+".jpg")
            #if (know_face_compare==-1):
            #    known_face_names.append(temp_name+".jpg")
            #    known_face_encodings.append(Face_id(know_face_compare))
            #else:
            #    known_face_encodings.append(Face_id[know_face_compare])
            

            
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord(' '):
        New_name = input('Please enter your name: ')
        j=Locate_Name(New_name)
        if (0<j):
            os.rename((name+".jpg"), (New_name+ len(known_face_encodings[j])+".jpg"))
            #known_face_names[j]=New_name
        else:
            os.rename((name+".jpg"),(New_name+".jpg"))
            known_face_names[Locate_Name(name)]=New_name
            

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
