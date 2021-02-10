import libjevois as jevois
import cv2 as cv
import numpy as np

## Finds Objects Of Color
#
# Add some description of your module here.
#
# @author Marc Peczka
# 
# @videomapping YUYV 320 240 60 YUYV 320 240 60 Foximus ObjectFinder
# @email 
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by Marc Peczka
# @mainurl 
# @supporturl 
# @otherurl 
# @license 
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class ObjectFinder:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        jevois.LINFO("ObjectFinder Constructor")
        self.frame = 0 # a simple frame counter used to demonstrate sendSerial()

    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        jevois.LFATAL("process no usb not implemented")

    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        jevois.LINFO("process with usb")

        # Get the next camera image (may block until it is captured):
        inimg = inframe.get()
        jevois.LINFO("Input image is {} {}x{}".format(jevois.fccstr(inimg.fmt), inimg.width, inimg.height))

        # Get the next available USB output image:
        outimg = outframe.get()
        jevois.LINFO("Output image is {} {}x{}".format(jevois.fccstr(outimg.fmt), outimg.width, outimg.height))

        # Example of getting pixel data from the input and copying to the output:
        jevois.paste(inimg, outimg, 0, 0)

        # We are done with the input image:
        inframe.done()

        Yellow_Lower = [10, 40, 100]
        Yellow_Upper = [50, 230, 255]

        lower = np.array(Yellow_Lower, dtype = "uint8")
        upper = np.array(Yellow_Upper, dtype = "uint8")

        # Example of in-place processing:
        #jevois.hFlipYUYV(outimg)
        src = jevois.convertToCvBGR(inimg)
        hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
        
        blur = cv.GaussianBlur(hsv, (3, 3), 0)
        
        mask = cv.inRange(hsv, lower, upper)
        
        canny_edge = cv.Canny(mask, 100, 200)
        
        rows = canny_edge.shape[0]
        circles = cv.HoughCircles(canny_edge, cv.HOUGH_GRADIENT, 1, 100,
                               param1=100, param2=20,
                               minRadius=5, maxRadius=75)
                               
        jevois.LINFO("CIRCLES: {}".format(circles))
        if outimg is not None:
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    center = (i[0], i[1])
                    #jevois.LINFO("TEST")
                    #jevois.LINFO("CIRCLE at {}".format(center))
                    centerx = i[0]
                    centery = i[1]
                    # circle center
                    cv.circle(src, center, 1, (0, 100, 100), 3)
                    #jevois.drawCircle(outimg, centerx, centery, 2, 1, 0)
                    # circle outline
                    radius = i[2]
                    cv.circle(src, center, radius, (255, 0, 255), 3)
                    #jevois.drawCircle(outimg, centerx, centery, radius, 1, 0)
        
        # Example of simple drawings:
        #jevois.drawCircle(outimg, int(outimg.width/2), int(outimg.height/2), int(outimg.height/4),
        #                  2, jevois.YUYV.White)
        #jevois.writeText(outimg, "Hi from Python - ObjectFinder", 20, 20, jevois.YUYV.White, jevois.Font.Font10x20)
        
        # Paste FPS onto img
        #info = jevois.getSysInfoCPU
        #jevois.writeText(outimg, center, 20, 20, jevois.YUYV.White, jevois.Font.Font10x20)
        # We are done with the output, ready to send it to host over USB:
        #jevois.drawCircle(outimg, 10, 10, 1, 1, 0)
        cv.circle(src, (20, 20), 20, (0, 100, 100), 3)
        jevois.convertCvBGRtoRawImage(src, outimg, 1)
        outframe.send()

        # Send a string over serial (e.g., to an Arduino). Remember to tell the JeVois Engine to display those messages,
        # as they are turned off by default. For example: 'setpar serout All' in the JeVois console:
        jevois.sendSerial("DONE frame {}".format(self.frame))
        self.frame += 1

    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    def parseSerial(self, str):
        jevois.LINFO("parseserial received command [{}]".format(str))
        if str == "hello":
            return self.hello()
        return "ERR: Unsupported command"
    
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "hello - print hello using python"

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    def hello(self):
        return "Hello from python!"
