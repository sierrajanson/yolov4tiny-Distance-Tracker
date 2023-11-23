import cv2

object_widths = {
    "person": 5, # person is face 
    "bicycle": 70,
    "car": 78,
    "motorbike": 60,
    "aeroplane": 200,
    "bus": 96,
    "train": 105,
    "truck": 96,
    "boat": 96,
    "traffic light": 20,
    "fire hydrant": 18,
    "stop sign": 24,
    "parking meter": 10,
    "bench": 48,
    "bird": 10,
    "cat": 16,
    "dog": 20,
    "horse": 60,
    "sheep": 36,
    "cow": 60,
    "elephant": 120,
    "bear": 60,
    "zebra": 80,
    "giraffe": 120,
    "backpack": 14,
    "umbrella": 36,
    "handbag": 12,
    "tie": 4,
    "suitcase": 24,
    "frisbee": 12,
    "skis": 72,
    "snowboard": 72,
    "sports ball": 8,
    "kite": 24,
    "baseball bat": 3,
    "baseball glove": 12,
    "skateboard": 10,
    "surfboard": 84,
    "tennis racket": 28,
    "bottle": 3,
    "wine glass": 4,
    "cup": 4,
    "fork": 1,
    "knife": 1,
    "spoon": 2,
    "bowl": 6,
    "banana": 2,
    "apple": 3,
    "sandwich": 4,
    "orange": 3,
    "broccoli": 6,
    "carrot": 1,
    "hot dog": 4,
    "pizza": 12,
    "donut": 4,
    "cake": 10,
    "chair": 24,
    "sofa": 84,
    "pottedplant": 12,
    "bed": 60,
    "diningtable": 96,
    "toilet": 15,  # Average width of a standard toilet bowl in inches
    "tvmonitor": 40,
    "laptop": 15,
    "mouse": 3,
    "remote": 6,
    "keyboard": 18,
    "cell phone": 2,
    "microwave": 20,
    "oven": 30,
    "toaster": 10,
    "sink": 30,
    "refrigerator": 36,
    "book": 8,
    "clock": 12,
    "vase": 8,
    "scissors": 4,
    "teddy bear": 6,
    "hair drier": 8,
    "toothbrush": 1
}
focal_length = 619.2                                                                    # need to configure for each camera, use below function

def set_focal_length(known_width, known_distance):
    """to estimate your camera's focal length, you need to know the width of an object in inches and the distance that it is from your camera"""
    # using focal length = (known distance of object from camera * object width pixel # on cv2 windows)/(known width of object)
    cap = cv2.VideoCapture(0)  
    ret,frame = cap.read()
    if not ret:
        print("Failed to read frame from the camera")
        return -1
    print("to be implemented soon....")

def find_screen_dimensions():                                                           # for debugging, returns number of pixels in width & height
    cap = cv2.VideoCapture(0)  
    width = int(cap.get(3))                                            
    height = int(cap.get(4))
    return f"{width} pixels wide and {height} pixels tall"

def find_distance(pixel, focal, known_width):                                           
    return (focal*known_width)/pixel

class DistanceByObject:
    def __init__(self, known_widths={}):
        self.fonts = cv2.FONT_HERSHEY_TRIPLEX                                           # font for displaying box descriptors to screen (cv2.putText())
        self.class_names = []
        self.known_widths = known_widths

        with open("classes.txt", "r") as objects_file:
            self.class_names = [e_g.strip() for e_g in objects_file.readlines()]
        yoloNet = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')             # yolov-tiny vision model that we are passing screen captures to make inferences
        self.model = cv2.dnn_DetectionModel(yoloNet)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    def detect_objects(self, object):
        classes, scores, boxes = self.model.detect(object,0.4,0.3)                      # all classes, their confidence scores, and their corresponding boxes retrieved from trained yolov4tiny model
        obj_list = []
        for (classid, score, box) in zip(classes, scores, boxes):                       # for each identified item, places rrectangle on screen
            cv2.rectangle(object, box,(0,0,255), 2)
            cv2.putText(object,"{}:{}".format(self.class_names[classid],format(score,'.2f')), (box[0], box[1]-14), self.fonts,0.6,(0,255,0), 3)
            obj_list.append([self.class_names[classid], box[2], (box[0], box[1]-2)])   # figure out what box is returning; i'm currently assuming pixel values        
        return obj_list                                                                # obj_list contains a bunch of obj_data items
    
    def vision_program_start(self):
        cap = cv2.VideoCapture(0)                                                   # captures image
        while True:                                                                 # until q is pressed, continuously identifies objects 
            ret,frame = cap.read()
            if not ret:
                print("Failed to read frame from the camera")
                break
            obj_data = self.detect_objects(frame)                   
            for d in obj_data:
                distance = 0
                try:
                    distance = find_distance(d[1],focal_length,self.known_widths[d[0]]) # pixels, focal length, known width
                except:                                                            # if we don't know what the object is
                    distance = find_distance(d[1],focal_length, 3)                 # can later work with vision to get them to pass how many inches wide the object is when vision doesn't recognize it 
                x,y = d[2]
                cv2.rectangle(frame, (x,y-3), (x+150, y+23),(255,255,255),-1)
                cv2.putText(frame,f"Distance:{format(distance,'.2f')}inchs", (x+5,y+13), self.fonts, 0.45,(255,0,0), 2)
                print("Distance of {} is {} inchs".format(d[0],distance))
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    my_obj = DistanceByObject(object_widths)
    my_obj.vision_program_start()

