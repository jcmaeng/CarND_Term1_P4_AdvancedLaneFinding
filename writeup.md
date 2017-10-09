# **Advanced Lane Finding Project**

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

[image1]: ./output_images/cal2-undistorted.jpg "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3-1]: ./output_images/p1_undist_orig.jpg "Original image"
[image3-2]: ./output_images/p2_hls_converted.jpg "HLS converted"
[image3-3]: ./output_images/p3_stacked_threshold.jpg "Stacked Threshold"
[image3-4]: ./output_images/p4_combined_s_gradient.jpg "Combined S Gradient"
[image3-5]: ./output_images/p5_warped_orig.jpg "Warped Original Image"
[image3-6]: ./output_images/p6_warped.jpg "Warped Lane Lines"
[image3-7]: ./output_images/p7_found_lines.jpg "Found Lane Lines"
[image3-8]: ./output_images/p8_result.jpg "Result"
[image4]: ./output_images/p7-1_lane_curvature.jpg "Lane Curvature"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[video1]: ./output_images/out_project.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the member function called camera_calibration() located in "lane_finding.py".  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

First of all, I convert the color space of undistorted road image to HLS and grayscale. Then I apply Sobel() to obtain thresholded x gradient and take thresholded data from S and L channels. With these data, I could  generate a binary image through combining color and gradient thresholds (thresholding steps at lines 385 through 414 in process_image() function). 
This image is undistorted original image.

![alt text][image3-1]

Below is the converted image to HLS color space.

![alt text][image3-2]

And the next two images show stacked threshold and combined S channel gradient.

![alt text][image3-3]
![alt text][image3-4]



#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 49 through 55 in the file `lane_finding.py` .  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points almost manually.

```python

src_pts = np.float32([[280,686], [595,455], [725,455], [1111,686]])
dst_pts = np.float32([[280, img_shape[0]], [280, 0], [1111, 0], [1111, img_shape[0]]])
```


This resulted in source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 280, 686      | 280, 720        | 
| 595, 455      | 280, 0      |
| 725, 455     | 1111, 0      |
| 1111, 686     | 1111, 720        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.
Below two images show the warped images from original image and generated one.

![alt text][image3-5]
![alt text][image3-6]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did use sliding window and fit my lane lines with a 2nd order polynomial kinda like this in example:

![alt text][image5]

This image shows found lane lines.

![alt text][image3-7]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in calculate_curvature() function at lines 289 through 340.

![alt text][image4]



#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in draw_lane_to_img() at lines 269 through 287 in my code. Here is an example of my result on a test image:

![alt text][image3-8]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result][video1]

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

In the step for applying threshold, I tried to use R/G channel in RGB color space, but it's not work properly so I removed that code.
And, after finishing implementation, I tried to test the 'challenge_video.mp4', it stoped in the middle of process because some data was not obtained properly.
There was no code for reusing previous data to find lane lines, and I added them and I could finish the process. However, the result movie of the challenge video did not show correct result.
Some method to obtain correct image in the step of applying threshold and find lane lines. I think that it is need to tune the threshold parameters.
