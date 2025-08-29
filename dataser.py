import cv2
import os

def create_dataset(output_dir, person_name, num_images=50):
    """
    Captures images from a webcam to create a labeled dataset.
    
    Args:
        output_dir (str): Path to save the dataset.
        person_name (str): Name/label of the person.
        num_images (int): Number of images to capture.
    """
    # Create the output directory if it doesn't exist
    person_dir = os.path.join(output_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Starting webcam. Press 'q' to quit.")
    
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Show the frame
        cv2.imshow(f"Capturing images for {person_name}", frame)

        # Save the frame as an image file
        if count < num_images:
            img_name = os.path.join(person_dir, f"{person_name}_{count+1}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"Image {count+1} saved at {img_name}")
            count += 1
        else:
            print(f"Captured {num_images} images for {person_name}.")
            break

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Process interrupted by user.")
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()
    print("Dataset collection complete.")


if __name__ == "__main__":
    # Directory where the dataset will be saved
    dataset_dir = r"C:\Users\varti\OneDrive\Desktop\project\student_images"

    # Ask for the label for the person (e.g., student's name)
    label_name = input("Enter the label (person's name) for the dataset: ").strip()

    # Ask for the number of images to capture
    try:
        num_images_to_collect = int(input("Enter the number of images to capture: "))
    except ValueError:
        print("Invalid number. Please enter a valid integer.")
        exit()

    # Call the function to create the dataset
    create_dataset(dataset_dir, label_name, num_images_to_collect)
