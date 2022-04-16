import cv2
import numpy as np

# TODO open handle to video file
stream = cv2.VideoCapture('kultisti.mp4')
# TODO font for drawing text
font = cv2.FONT_HERSHEY_SIMPLEX
# player color range in HSV
playerLo = np.array([25, 50, 50])
playerHi = np.array([35, 255, 255])

# top of purple floor color range in HSV
floorLo = np.array([150, 50, 50])
floorHi = np.array([160, 255, 255])

# TODO read the stream frame by frame
while stream.isOpened():
    # TODO read frame
    ret, frame = stream.read()
    # TODO change color spaces from RGB to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # TODO mask out the player color range
    playerMask = cv2.inRange(hsv, playerLo, playerHi)
    # TODO caculate the center via moments
    # TODO get moments from player mask
    M = cv2.moments(playerMask)
    if M["m00"] != 0:
        # this part directly taken from docs
        # the mathematically inclined amongus
        # might wanna go learn around moments (optional)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print(cX, cY)
        # TODO draw some cute graphics
        frame = cv2.putText(frame, f'player = ({cX}, {cY})', (0, 48), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        frame = cv2.circle(frame, (cX, cY), 20, (0, 0, 255), 2)
    # TODO mask out the floor color range
    floorMask = cv2.inRange(hsv, floorLo, floorHi)

    # TODO imshow some intermediate frames to see whats going on
    cv2.imshow('frame', frame)
    # early termination condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# TODO cleanup
stream.release()
cv2.destroyAllWindows()
