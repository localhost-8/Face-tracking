#Face tracker using OpenCV and Arduino
# by staffuser
import cv2
import serial,time
def main():
    while True:
        face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap=cv2.VideoCapture(0)
        #fourcc= cv2.VideoWriter_fourcc(*'XVID')
        # ArduinoSerial=serial.Serial('com7',9600,timeout=0.1)
        #out= cv2.VideoWriter('face detection4.avi',fourcc,20.0,(640,480))
        time.sleep(1)
        while cap.isOpened():
            ret, frame= cap.read()
            frame=cv2.flip(frame,1)  #mirror the image (зеркало изображения)
            #print(frame.shape)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # конвертируем изображение в серое
            faces= face_cascade.detectMultiScale(gray,1.1,6)  #detect the face (обнаруживаем лицо)
            for x,y,w,h in faces:
                #sending coordinates to Arduino (передаем координаты в Arduino)
                string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
                print(string)
                # ArduinoSerial.write(string.encode('utf-8'))
                #plot the center of the face
                cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
                #plot the roi (рисуем область, существенную для анализа)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
                faces = frame[y:y + h, x:x + w]
            #plot the squared region in the center of the screen (рисуем белый прямоугольник в центре изображения)
            #'''
            #'''
            cv2.rectangle(frame,(640//2-30,480//2-30),
                         (640//2+30,480//2+30),
                          (255,255,255),3)
            
            try:
                # set a new height in pixels
                new_height = 100

                # dsize
                dsize = (faces.shape[1], new_height)
                output = cv2.resize(faces, dsize, interpolation = cv2.COLOR_BGR2GRAY)
                cv2.imshow('img',output)
            except:
                cv2.imshow('img',frame)
            #cv2.imwrite('output_img.jpg',frame)
            for testing purpose:
                read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
                time.sleep(0.05)
                print('data from arduino:'+read)

            # press q to Quit (нажмите q для выхода из программы)
            if cv2.waitKey(1)&0xFF== ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
main()

#https://github.com/staffuser