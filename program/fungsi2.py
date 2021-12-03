import cv2
# Dlib adalah suatu library berfungsi dengan cara menganalisis bagian wajah
# dengan mengekstrak nilai gambar (Niu & Chen, 2018). Dengan mengekstrak nilai pada wajah manusia
# dlib akan menghasilkan 128 dimensional feature vektor (Chen & Sang, 2018). Dlib akan digunakan untuk membantu
# mengolah gambar wajah pada metode facial landmark.
# dlib digunakan untuk memeprkirakan lokasi koordinat kendaraan (x,y) dan akan mengembalikan objek bentuk yang mengandung (x, y)

import dlib

carCascade = cv2.CascadeClassifier('kendaraan.xml')
video = cv2.VideoCapture('footage\carss.mp4')

WIDTH = 1280
HEIGHT = 720


def cariObject():
    warnaKotak = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0

    carTracker = {}
    carLocation1 = {}
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

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)

        if not (frameCounter % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 2.2, 13, 189)
            # gray  merupakan matriks yang berisi gambar tempat objek terdeteksi
            # 2.2 merupakan parameter yang menentukan seberapa besar ukuran gambar diperkecil pada setiap skala gambar.
            # 13 merupakan objek yang ukurannya kurang dari itu akan diabaikan minsize
            # 189 merupakan objek yang ukurannya lebih besar dari angka tersebut akan diabaikan

            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h
                # agar kotakkan pada koordinat x dan y sejajar dengan w dan h dan tidak saling acak atau bertumpuk

                matchCarID = None
                # None adalah sebuah tipe data spesial yang menunjukkan bahwa nilai/data suatu variabel itu belum/tidak ada (bukan nol, tapi tidak ada)

                # FUNGSI 1
                # agar kotakkan kendaraan tidak ketinggalan
                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (
                            x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                # FUNGSI 2
                        matchCarID = carID
                if matchCarID is None:
                    pelacakan = dlib.correlation_tracker()
                    # dlib digunakan untuk memperkirakan kotakkan dengan koordinat x dan y
                    pelacakan.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = pelacakan
                    carLocation1[currentCarID] = [x, y, w, h]
                    currentCarID = currentCarID + 1
                # Perubahan nilai pada variabel currenID akan bertambah satu dalam penjumlahan kendaraan secara berulang.

        # FUNGSI DUA

        cv2.line(resultImage, (200, 480), (1200, 480), (0, 255, 255), 3)

        # 200 merupakan margin kiri ke kanan
        # 480 merupakan garis diagonal dari kanan ke bawah dari atas ke bawah
        # 1200 merupakan margin atau jarak garis dari kanan ke kiri
        # 0,255,255 merupakan warna dari BGR dengan kombinasi warna hijau dan merah

        cv2.putText(resultImage, 'Jumlah Kendaraan: ' + str(int(currentCarID)), (230, 460), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (255, 0, 0), 2)

        # 230 merupakan margin atau jarak dari kiri ke kanan
        # 460 merupakan margin jarak ketinggian dari text "jumlah kendaraan" dari atas ke bawah
        # 0,75 merupakan ukuran font
        # 255,0,0 merupakan warna dari BGR
        # 2 merupakan ukuran ketebalan dari text tersebut

        for carID in carTracker.keys():
            # keys untuk mengambil fungsi kunci elemen dictionary
            trackedPosition = carTracker[carID].get_position()

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())

            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), warnaKotak, 2)

        # Menampilkan display
        cv2.imshow('Output', resultImage)

        # fungsi pengikat keyboard. Maksutnya adalah waktu dalam milidetik.

        if cv2.waitKey(1) & 0xcFF == ord('q'):
            break
            # ord untuk mengembalikan integer yang merupakan kode karakter unicode dari sebuah string karakter yang menjadi argumennya
            # & merupakan operasi bitwise biangan operator yang melakukan operasi berdasarkan bit


if __name__ == '__main__':
    cariObject()
