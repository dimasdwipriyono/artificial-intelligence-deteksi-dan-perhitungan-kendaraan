import cv2
import dlib

vehicleCascade = cv2.CascadeClassifier('kendaraan.xml')
video = cv2.VideoCapture('footage\carss.mp4')

WIDTH = 1280
HEIGHT = 720

def cariObject():
    warnaKotak = (0, 255, 0)
    frameCounter = 3
    arusKendaraan = 0
    pelacakKendaraan = {}
    lokasiKendaraan1 = {}
    carLocation2 = {}

    # FUNGSI SATU
    while True:
        rc, image = video.read()
        if type(image) == type(None):
            break

        image = cv2.resize(image, (WIDTH, HEIGHT))
        resultImage = image.copy()

        frameCounter = frameCounter + 1

        carIDtoDelete = []

        for carID in pelacakKendaraan.keys():
            trackingQuality = pelacakKendaraan[carID].update(image)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            pelacakKendaraan.pop(carID, None)
            lokasiKendaraan1.pop(carID, None)
            carLocation2.pop(carID, None)

        if not (frameCounter % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = vehicleCascade.detectMultiScale(gray, 2.2, 13, 189)
            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h


                # FUNGSI 2

                matchCarID = None
                for carID in pelacakKendaraan.keys():
                    trackedPosition = pelacakKendaraan[carID].get_position()
                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())
                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (
                            x <=(x + w)) and (y <= (y + h))):

                        matchCarID = carID
                if matchCarID is None:
                    pelacakan = dlib.correlation_tracker()
                    pelacakan.start_track(image, dlib.rectangle(x, y, x + w, y + h))
                    pelacakKendaraan[arusKendaraan] = pelacakan
                    lokasiKendaraan1[arusKendaraan] = [x, y, w, h]
                    arusKendaraan = arusKendaraan + 1

        cv2.line(resultImage, (200, 480), (1200, 480), (0, 255, 255), 3)
        cv2.putText(resultImage, 'Jumlah Kendaraan: ' + str(int(arusKendaraan)), (230, 460), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (255, 0, 0), 2)
        for carID in pelacakKendaraan.keys():
            trackedPosition = pelacakKendaraan[carID].get_position()
            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())
            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), warnaKotak, 2)

        cv2.imshow('Video', resultImage)
        if cv2.waitKey(1) & 0xcFF== ord('q'):
            break

if __name__ == '__main__':
    cariObject()
