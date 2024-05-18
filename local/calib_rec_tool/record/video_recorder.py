from typing import Tuple
import cv2
import os


def record_video(
    output_filepath: str,
    frame_res: Tuple[int, int] = (640, 480),
    fps: float = 20.0,
    duration: float = 10,
):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        os.path.join(output_path, output_filename),
        fourcc,
        fps,
        frame_res,
    )

    # Open the default webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_res[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_res[1])

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(
        f"Recording video to {os.path.join(output_path, output_filename)} for {duration} seconds..."
    )

    # Record video for the specified duration
    num_frames = int(fps * duration)
    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        out.write(frame)

        # Display the resulting frame
        cv2.imshow("Recording...", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("Recording complete.")


if __name__ == "__main__":
    output_path = input("Enter the output directory: ")
    output_filename = input("Enter the output filename (e.g., output.avi): ")
    duration = int(input("Enter the duration of the video in seconds: "))

    record_video(os.path.join(output_path, output_filename), duration=duration)
