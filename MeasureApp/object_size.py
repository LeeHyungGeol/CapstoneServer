# USAGE
# python object_size.py --image images/example_01.png --width 0.955
# python object_size.py --image images/example_02.png --width 0.955
# python object_size.py --image images/example_03.png --width 3.5

# import the necessary packages
import sys
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
from ar_markers import detect_markers
import os
from uuid import uuid4
from django.utils import timezone
from .models import MeasureHistory
from .serializers import MeasureHistorySerializer

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)




def measure_length(url, user) :
	# construct the argument parse and parse the arguments
	# ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--image", required=True,
	# 	help="path to the input image")
	# ap.add_argument("-w", "--width", type=float, required=True,
	# 	help="width of the left-most object in the image (in inches)")
	# args = vars(ap.parse_args())

	# load the image, convert it to grayscale, and blur it slightly
	flag = True
	img_url = url
	print("image url :", img_url)
	image = cv2.imread('./'+img_url)

	markers = detect_markers(image)
	marker_width = 15

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)
	# cv2.imshow("gaussian", gray)

	# ret, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# cv2.imshow("binary", gray)

	# perform edge detection, then perform a dilation + erosion to
	# close gaps in between object edges
	edged = cv2.Canny(gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	print(len(cnts))

	# sort the contours from left-to-right and initialize the
	# 'pixels per metric' calibration variable
	(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
	print(len(cnts))

	cnts = list(cnts)
	try:
		cnts.insert(0, markers[0].contours)
	except Exception:
		print("marker detection fail")
		flag = False
		return flag
		# sys.exit()

	cnts = tuple(cnts)
	print(len(cnts))

	pixelsPerMetric = None

	# loop over the contours individually
	result_list = list()
	for idx,c in enumerate(cnts):

		# if the contour is not sufficiently large, ignore it
		if cv2.contourArea(c) < 100:
			continue

		# compute the rotated bounding box of the contour
		orig = image.copy()
		box = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")

		# order the points in the contour such that they appear
		# in top-left, top-right, bottom-right, and bottom-left
		# order, then draw the outline of the rotated bounding
		# box
		box = perspective.order_points(box)
		cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

		# loop over the original points and draw them
		for (x, y) in box:
			cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

		# unpack the ordered bounding box, then compute the midpoint
		# between the top-left and top-right coordinates, followed by
		# the midpoint between bottom-left and bottom-right coordinates
		(tl, tr, br, bl) = box
		(tltrX, tltrY) = midpoint(tl, tr)
		(blbrX, blbrY) = midpoint(bl, br)

		# compute the midpoint between the top-left and top-right points,
		# followed by the midpoint between the top-righ and bottom-right
		(tlblX, tlblY) = midpoint(tl, bl)
		(trbrX, trbrY) = midpoint(tr, br)

		# draw the midpoints on the image
		cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

		# draw lines between the midpoints
		cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
			(255, 0, 255), 2)
		cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
			(255, 0, 255), 2)

		# compute the Euclidean distance between the midpoints
		dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
		dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

		# if the pixels per metric has not been initialized, then
		# compute it as the ratio of pixels to supplied metric
		# (in this case, inches)
		if pixelsPerMetric is None:
			pixelsPerMetric = dB / marker_width


		# compute the size of the object
		dimA = dA / pixelsPerMetric
		dimB = dB / pixelsPerMetric

		# draw the object sizes on the image




		# show the output image
		if (float(format(dimA)) > 25 or float(format(dimB)) > 25):
			if idx == 0:
				continue

			cv2.putText(orig, "width: {:.1f}cm".format(dimB),
						(0, 100), cv2.FONT_HERSHEY_SIMPLEX,
						1.2, (255, 0, 0), 2)
			cv2.putText(orig, "height: {:.1f}cm".format(dimA),
						(0, 150), cv2.FONT_HERSHEY_SIMPLEX,
						1.2, (255, 0, 0), 2)

			save_path = date_upload_measured()
			print('save path:' + save_path)
			cv2.imwrite('./media/' + save_path, orig)

			img_measured = MeasureHistory.objects.create(user_idx = user, image = save_path, width = dimB, height = dimA )
			img_measured.save()
			img_measured.msg = '성공'
			img_measured.code =100
			result_list.append(img_measured)

	return result_list


def date_upload_measured():
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    # extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        'measure',
        ymd_path,
        uuid_name + '.jpg'
        ])