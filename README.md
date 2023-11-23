# yolov4tiny-Distance-Tracker

Work for Slugbotics ARM team: Can identify a range of objects and their distance from your camera in inches based on the estimated width of the object (inches). 

Current issues: distance calculations for non-rectangularly shaped objects (humans) is inaccurate due to that humans can not be encompassed by a single width.
Options considering: calculating width of objects in camera's field based on the width of a recognized object..
(this could be useful for us in cases where the arm does not recognize an object; we can provide the arm more identifying information (color, approximate size) and use the above to calculate the width and thus estimate the distance)
