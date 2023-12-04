import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, etc.
# model = torch.hub.load('ultralytics/yolov5', 'custom', 'path/to/best.pt')  # custom trained model

# Images
im = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, URL, PIL, OpenCV, numpy, list

# Inference
results = model(im)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

results.xyxy[0]  # im predictions (tensor)
print (results.pandas().xyxy[0].name)