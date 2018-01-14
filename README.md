## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/calibration_output.jpg "Calibration Output"
[image2]: ./output_images/undistort.png "Undistort"
[image3]: ./output_images/test_images/undistort.png "Undistort Test Image"
[image4]: ./output_images/test_images/clr_grd_threshold.png "Thresholded Image"
[image5]: ./output_images/test_images/region.png "Region Image"
[image6]: ./output_images/test_images/warp.png "Warped Image"
[image7]:  ./output_images/test_images/bin_warp.png "Bin Warped Image"
[image8]:  ./output_images/test_images/find_lines.png "Find Lines on test images"
[image9]:  ./output_images/test_images/find_prev_lines.png "Find Lines on test images"
[image10]:  ./output_images/test_images/final_test_images.png "Final Images after pipeline"
[video1]: ./output_videos/project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You are reading it!
The code implementation is located in [this](./AdvancedLaneLines.ipynb) jupyter notebook.

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the **Camera calibration** section of the python notebook.
I used the provided [calibration images](./camera_cal) which picture a chessboard image. Its high contrast pattern makes it easy to detect the corners and use them in the `cv2.calibrateCamera` which will help with our calibration.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image. Then `imgpoints` were appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection. An example of detection is shown below:

![alt text][image1]

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

![alt text][image2]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

So after I found out the calibration parameters (the camera matrix `mtx` and the distortion coefficients `dist` ) for the camera was time to use them to "undistort" the test images provided. The step was rather straight forward as it required only to use the `cv2.undistort()` once again with the same parameters. An example of an "undistorted" test image is shown below:

![alt text][image3]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image. The helper functions as well as the final thresholding function `img_thr` is located in **Apply Gradients** section of the notebook. I experimented with a large number of combinations. I used most of the helper functions that were introduced in the lesson. The final combination that helped me get the best results was:

* Y channel binary of the YUV which helped me a lot with detecting the white lines even in low contrast conditions (e.g. shadows or very light colored tarmac.)
* B channel binary of the LAB which helped a lot on yellow lines on conditions like the previous. These two colorspace binaries were combined together in an *OR* statement.
* A combination of different sobel thresholding on both derivatives was also combined with the S channel of the HLS colorspace gave the opportunity to get rid most of the shadows and false *low contrast* edges that could confuse our line detection afterwards.

The result of the thresholding can be seen below

![alt text][image4]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in section **Perspective Transform** of python notebook. The `warper()` function takes as inputs an image (`img`), and the conversion matrix (`M`). The matrix `M` is generated from the function `cv2.getPerspectiveTransform()` which gets as input the source `src` and the `destination` points.
I chose to hardcode the source and destination points in the following manner:

```python

x = 1280
y = 720

src_bl = [x*0.140, y*1.00] # Source Bottom Left
src_br = [x*0.880, y*1.00] # Source Bottom Right
src_tr = [x*0.561, y*0.65] # Source Top Right
src_tl = [x*0.443, y*0.65] # Source Top Left

src = np.array([[src_bl, src_br, src_tr, src_tl]], dtype=np.float32)

dst_bl = [(x//2)-310, y] # Destination Bottom Left
dst_br = [(x//2)+310, y] # Destination Bottom Right
dst_tr = [(x//2)+310, 0] # Destination Top Right
dst_tl = [(x//2)-310, 0] # Destination Top Left

dst = np.array([[dst_bl, dst_br, dst_tr, dst_tl]], dtype=np.float32)
```

The destination points actual are created by taking the center of image which is 640 and applying the same offset left and right and they are located in `y=0` and `y=720` which is the image height. The source points were created by trial and error by checking the result on a regioned image like the image below:

![alt text][image5]

This resulted in the following source and destination points:

|Point         | Source      | Destination   |
|:------------:|:-----------:|:-------------:|
| Bottom Left  | 179.2, 720  | 330, 720      |
| Bottom Right | 1126.4, 720 | 950, 720      |
| Top Right    | 718.08, 468 | 950, 0        |
| Top Left     | 567.04, 468 | 330, 0        |


I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image6]


#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

In order to find the lines in my image I had first to run the whole image processing so far that resulted in a binary warped image as the one below:

![alt text][image7]

Then I created the `find_lines` and `find_prev_lines` functions located in **Locating Lines** section of the notebook.

The `find_lines` given a warped image and some parameters like the number of sliding windows, the margin of their width and the minimum number of pixels to recenter window is able return the lines using histogram detection. This function was created to be used at fresh start of line detection sequence when no previous knowledge about the location of the lines exists.
If there are previous line detections the `find_prev_lines` function is used which takes the previous lines and calculates the new ones.

The result can be shown on the picture below:

**`find_lines` Visualization**
![alt text][image8]
**`find_prev_lines` Visualization**
![alt text][image9]


#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

In order to calculate the curvature I created a function `calc_curvature` which is defined in section **Draw lane and Calculate curvature** of the notebook. To measure the radius of curvature of the polynomial curves closest to the vehicle, I used the y curve values of the bottom of each image. I then calculated the curvature for each line (left and right). The lane curvature is the average of the two curvatures. In order to transform the units from pixels to meters I firstly estimated the `ym_per_pix` taking into account that a short lane line has about 3 meters length. For the `xm_per_px` as long as there is information I use the difference between the left and right lines and the knowledge tha the lane in real life is approximately 3.7 meters. If there is no difference between the lines available I get a default value of 620 pixels which corresponds on my lane width on a warped image. Finally I calculate the distance from center by assuming that the real lane center is located in the middle of the image.


#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in **Test on images** section of the notebook. I created a class `Processor` with the `processImage` member function keeping in mind that it will be later used in video processing. The `processImage` includes all the pipeline:

* Undistort the original image
* Apply thresholds to the undistorted image8
* Warp the binary image
* Find the lines by:
  * Using the `find_lines` if it is a clear start
  * Using the `find_prev_lines` if there are previously detected Lines
* Calculate the curvature and distance from center.
* Draw the lines and the Lane
* Unwarp the image using the inverse perspective matrix.
* Print the debug info (curvature distance from center) on the frame.


The result of the pipeline for all the images can be shown below:


![alt text][image10]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./output_videos/project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Some issues I faces during the implementation are the following:

* Curvature values on straight lines hit an extreme high. This is good and bad. It is good because given the tangent of a vertical line cannot be defined the algorithm seems to work well. On the other hand it would be good if these high values could be filtered out.
* The line detection is not so smooth at some points. Perhaps it could help if there is a history of the measurements and as the project indicated a Line class which keeps track of history could eliminate such an issue.
* Another issue which could occur in different situations like driving up or down a hill where the perspective changes. In that case the current perspective matrix is of no use. Perhaps it would be better if the periodically the matrix is calculated in the pipeline given some known points from previous frames.
* Also the thresholding is done only taking account images of certain weather conditions. Perhaps it would be more robust if the thresholding parameters were trained using a neural network and a dataset of many different lane pictures.
