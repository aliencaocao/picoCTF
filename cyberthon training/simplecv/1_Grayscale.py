import cv2

# open handle to video file
stream = cv2.VideoCapture('kultisti.mp4')

# simple grayscale processing example
while(stream.isOpened()):
    # read frame
    ret, frame = stream.read()

    # draw the frame
    cv2.imshow('frame', frame)
    
    # make frame gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #draw the gray scale frame
    cv2.imshow('gray', gray)
    
    # early termination condition
    # press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()