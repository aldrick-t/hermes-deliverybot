import cv2
import numpy as np
import glob

def calibrate_camera(calibration_images_folder, chessboard_size=(9,6), square_size=0.025):
    objp = np.zeros((chessboard_size[1]*chessboard_size[0], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0],
                          0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []

    images = glob.glob(f'{calibration_images_folder}/*.jpg')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
                                        (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
            imgpoints.append(corners2)

            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
            cv2.imshow('Calibration', img)
            cv2.waitKey(100)

    cv2.destroyAllWindows()

    ret, camera_matrix, distortion_coeff, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    if ret:
        print("Camera calibration was successful.")
        print("Camera matrix:")
        print(camera_matrix)
        print("\nDistortion coefficients:")
        print(distortion_coeff)
        np.savez("calibration_data.npz", camera_matrix=camera_matrix, distortion_coeff=distortion_coeff)
    else:
        print("Camera calibration failed.")

    return ret, camera_matrix, distortion_coeff, rvecs, tvecs

if __name__ == "__main__":
    calibrate_camera('calibration_images', (9,6), 0.025)