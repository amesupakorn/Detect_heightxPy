'''full'''
import cv2

cam_port = 0
cam = cv2.VideoCapture(0)
total, dic_pic = 1, dict()
body_model = cv2.CascadeClassifier('body_detec.xml')
# img = cv2.imread('photo1,jpg')
# gray_scal = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2GRAY)
# human = body_model.detectMultiScale(gray_scal)




face_track = cv2.CascadeClassifier('face_alt.xml')


while True:
    result, image = cam.read()
    cv2.imshow("photo", image)
    if cv2.waitKey(1) & 0x0FF == ord("q"):
        cv2.imwrite("photo%d.png"%total, image)
        img = cv2.imread("photo%d.png" %total)
        gray_scal = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x, y, w, h = (face_track.detectMultiScale(gray_scal))[0]
        dic_pic['photo'+str(total)+'.png'] = y
        total += 1
    if cv2.waitKey(1) & 0x0FF == ord("d"):
        break
print(dic_pic)
