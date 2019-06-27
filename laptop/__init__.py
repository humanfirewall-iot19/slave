import cv2
import os

WNAME = "HumanFirewall Test"

board_id = os.getenv("BOARD_ID")
if board_id is None: board_id = 1234

print(" [baord_id =", board_id, "]")

slave_callback = lambda x: None

def get_id():
    global board_id
    return board_id

def register_handler(cb):
    global slave_callback
    slave_callback = cb

def device_setup_and_idle():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow(WNAME, cv2.WINDOW_NORMAL)
    #cv2.resizeWindow(WNAME, 1400,900)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow(WNAME, frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "images/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            
            slave_callback(img_name)

    cam.release()
    cv2.destroyAllWindows()

