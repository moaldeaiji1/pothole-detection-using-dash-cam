# pothole-detection-using-dash-cam

# OBJECTIVES
The objective of this project is to use available videos to detect potholes and generate PDF reports that include GPS information. This involves the following key tasks:

1-Pothole Detection: Utilize video data to identify and detect potholes accurately. 				

2-Report Generation: Create detailed PDF reports that document the detected potholes.

3-GPS Integration: Include GPS information in the reports to provide precise location details of the potholes.

This approach will ensure a comprehensive and informative report on the pothole occurrences, aiding in efficient maintenance and repair.


# ![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/daa99e46-8d67-4b43-b49a-e038e60ccdb2)
The model was trained using YOLOv8 with publicly available data.



![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/9c077416-e390-4f5d-bdab-1ca4394e1d0e)

We trained two models: for weaker PCs, we trained YOLOv8n, and for powerful PCs, we trained YOLOv8l.

YOLOv8n will be faster but less accurate, while YOLOv8l will be slower but more accurate.


# Interface
simple interface for the user, click or drag and drop to start processing, user can chose multiple videos . 
![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/afbe1f85-cdd6-4d10-b375-6c775b064a02)




easy to change models.



![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/c63bafe7-363a-47d3-9116-bc8acfe20add)


Easy to show folder of generated PDF files.
![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/48846635-c20d-4bb0-8f08-c4da799dad48)



Interface showing progress videos, percentage of each video, and buttons to cancel processing or pause.
![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/0b0affcf-844a-45a0-9f29-8c1d43905337)








PDF generated with GPS information.


![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/65872713-b12a-4ea5-8b05-784697f12f2d)







# limtaion 
1-Most images used to train the model were not taken with a dash cam angle, hence it would be difficult to detect.

2-The reflection will cause random detection 

![image](https://github.com/moaldeaiji1/pothole-detection-using-dash-cam/assets/164229271/53d89522-f5e2-49d3-aa60-469d13f914d6)


3-The qualty of the images need to be improved 

















