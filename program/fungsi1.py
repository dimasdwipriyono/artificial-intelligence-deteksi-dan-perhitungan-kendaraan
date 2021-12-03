import cv2
import dlib

#mesin learning atau algoritma dari kendaraan
carCascade = cv2.CascadeClassifier('kendaraan.xml')
video = cv2.VideoCapture('footage\carss.mp4')

#panjang dan lebar dalam satuan pixel
WIDTH = 1280
HEIGHT = 720


def trackMultipleObjects():
	rectangleColor = (0, 255, 0)
	frameCounter = 0
	currentCarID = 0
	carTracker = {}
	carLocation1 = {}

	while True:
		rc, image = video.read()
		if type(image) == type(None):
			break

		image = cv2.resize(image, (WIDTH, HEIGHT))
		resultImage = image.copy()

		frameCounter = frameCounter + 1

		carIDtoDelete = []

		for carID in carTracker.keys():
			trackingQuality = carTracker[carID].update(image)

			if trackingQuality < 4:
				carIDtoDelete.append(carID)

		if not (frameCounter % 10):
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

			for (_x, _y, _w, _h) in cars:
				x = int(_x)
				y = int(_y)
				w = int(_w)
				h = int(_h)

				matchCarID = None

				if matchCarID is None:
					tracker = dlib.correlation_tracker()
					tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

					carTracker[currentCarID] = tracker
					carLocation1[currentCarID] = [x, y, w, h]
					currentCarID = currentCarID + 1

		for carID in carTracker.keys():
			trackedPosition = carTracker[carID].get_position()

			t_x = int(trackedPosition.left())
			t_y = int(trackedPosition.top())
			t_w = int(trackedPosition.width())
			t_h = int(trackedPosition.height())

			cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

		cv2.imshow('result', resultImage)

		if cv2.waitKey(33) == 27:
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	trackMultipleObjects()
