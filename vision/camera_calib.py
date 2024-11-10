import cv2
import numpy as np
import glob

def calibrate_camera(calibration_images_folder, chessboard_size=(9,6), square_size=0.025):
    """
    Calibrate the camera using multiple images of a chessboard pattern.

    Parameters:
        calibration_images_folder (str): Path to the folder containing calibration images.
        chessboard_size (tuple): Number of inner corners per a chessboard row and column (columns, rows).
        square_size (float): Size of a square in your defined unit (e.g., meters).

    Returns:
        ret (bool): Whether calibration was successful.
        camera_matrix (numpy.ndarray): The camera matrix.
        distortion_coeff (numpy.ndarray): The distortion coefficients.
        rvecs (list): Rotation vectors.
        tvecs (list): Translation vectors.
    """
    # Prepare object points based on the actual size of your calibration pattern
    objp = np.zeros((chessboard_size[1]*chessboard_size[0], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0],
                          0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size  # Scale object points by square size

    # Arrays to store object points and image points from all the images
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in image plane

    # Get list of calibration images
    images = glob.glob(f'{calibration_images_folder}/*.jpg')  # Adjust the extension if needed

    if not images:
        print(f"No images found in {calibration_images_folder}.")
        return False, None, None, None, None

    for fname in images:
        img = cv2.imread(fname)
        if img is None:
            print(f"Failed to load image {fname}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            # Refine corner locations
            criteria = (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
            cv2.imshow('Calibration', img)
            cv2.waitKey(100)  # Display each image for 100ms
        else:
            print(f"Chessboard couldn't be found in image {fname}")

    cv2.destroyAllWindows()

    if not objpoints or not imgpoints:
        print("No corners were found in any image. Calibration failed.")
        return False, None, None, None, None

    # Perform camera calibration
    ret, camera_matrix, distortion_coeff, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    if ret:
        print("Camera calibration was successful.")
        print("Camera matrix:")
        print(camera_matrix)
        print("\nDistortion coefficients:")
        print(distortion_coeff)
    else:
        print("Camera calibration failed.")

    return ret, camera_matrix, distortion_coeff, rvecs, tvecs

def save_calibration_data(filename, camera_matrix, distortion_coeff):
    """
    Save the calibration data to a file.

    Parameters:
        filename (str): Path to the file where data will be saved.
        camera_matrix (numpy.ndarray): The camera matrix.
        distortion_coeff (numpy.ndarray): The distortion coefficients.
    """
    np.savez(filename, camera_matrix=camera_matrix, distortion_coeff=distortion_coeff)
    print(f"Calibration data saved to {filename}")

def load_calibration_data(filename):
    """
    Load calibration data from a file.

    Parameters:
        filename (str): Path to the file containing calibration data.

    Returns:
        camera_matrix (numpy.ndarray): The camera matrix.
        distortion_coeff (numpy.ndarray): The distortion coefficients.
    """
    data = np.load(filename)
    camera_matrix = data['camera_matrix']
    distortion_coeff = data['distortion_coeff']
    return camera_matrix, distortion_coeff

if __name__ == "__main__":
    # Specify the folder containing calibration images
    calibration_images_folder = 'calibration_images'  # Replace with your folder path

    # Perform calibration
    ret, camera_matrix, distortion_coeff, rvecs, tvecs = calibrate_camera(
        calibration_images_folder,
        chessboard_size=(9,6),
        square_size=0.025  # Example: 25mm squares
    )

    if ret:
        # Save the calibration data for later use
        save_calibration_data('calibration_data.npz', camera_matrix, distortion_coeff)
    else:
        print("Calibration was unsuccessful. Please check your images and try again.")