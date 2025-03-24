import os
import cv2
from tkinter import *
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess

# Paths to the Excel files
attendance_path = r"C:\Users\varti\Downloads\face_recogniton-learnFromBasics-main\attendance.xlsx"
intruder_log_path = r"C:\Users\varti\Downloads\face_recogniton-learnFromBasics-main\face_recogniton-learnFromBasics-main\intruders.xlsx"
dataset_dir = r"C:\Users\varti\OneDrive\Desktop\project\student_images"  # Directory to save dataset

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x768+100+50")
        self.root.title("Face Recognition System")

        # Header image
        header_img_path = r"C:\Users\varti\OneDrive\Desktop\project\img\bg1.jpg"
        if not os.path.exists(header_img_path):
            messagebox.showerror("Error", f"Header image not found: {header_img_path}")
            self.root.destroy()
            return

        header_img = Image.open(header_img_path)
        header_img = header_img.resize((1024, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(header_img)
        header_label = Label(self.root, image=self.photoimg)
        header_label.place(x=0, y=0, width=1024, height=130)

        # Background image
        bg_img_path = r"C:\Users\varti\OneDrive\Desktop\project\img\bg1.jpg"
        if not os.path.exists(bg_img_path):
            messagebox.showerror("Error", f"Background image not found: {bg_img_path}")
            self.root.destroy()
            return

        bg_img = Image.open(bg_img_path)
        bg_img = bg_img.resize((1024, 768), Image.Resampling.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg_img)
        bg_label = Label(self.root, image=self.photobg1)
        bg_label.place(x=0, y=130, width=1024, height=768)

        # Title section
        title_label = Label(
            bg_label,
            text="Face Recognition System",
            font=("verdana", 25, "bold"),
            bg="white",
            fg="navyblue"
        )
        title_label.place(x=0, y=0, width=1024, height=45)

        # Buttons with absolute image paths
        self.create_button(bg_label, r"C:\Users\varti\OneDrive\Desktop\project\img\student.jpg", "Student Dataset", self.create_student_dataset, 250, 100)
        self.create_button(bg_label, r"C:\Users\varti\OneDrive\Desktop\project\img\face.jpg", "Face Recognition", self.face_rec, 480, 160)
        self.create_button(bg_label, r"C:\Users\varti\OneDrive\Desktop\project\img\att.jpg", "Attendance", self.open_attendance_sheet, 710, 100)
        self.create_button(bg_label, r"C:\Users\varti\OneDrive\Desktop\project\img\intruder.jpg", "Intruder", self.open_intruder_log, 250, 330)
        self.create_button(bg_label, r"C:\Users\varti\OneDrive\Desktop\project\img\exi.jpg", "Exit", self.Close, 710, 330)

    def create_button(self, parent, img_path, text, command, x, y):
        """Utility function to create a button with an image and label."""
        if not os.path.exists(img_path):
            messagebox.showerror("Error", f"Button image not found: {img_path}")
            return

        img = Image.open(img_path)
        img = img.resize((180, 180), Image.Resampling.LANCZOS)
        photo_img = ImageTk.PhotoImage(img)

        btn = Button(parent, image=photo_img, command=command, cursor="hand2")
        btn.image = photo_img  # Keep reference to avoid garbage collection
        btn.place(x=x, y=y, width=180, height=180)

        label = Button(
            parent,
            text=text,
            command=command,
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        label.place(x=x, y=y + 180, width=180, height=45)

    def create_student_dataset(self):
        """Capture images using webcam and save them to a dataset directory."""
        # Ask the user for the person's name
        person_name = simpledialog.askstring("Input", "Enter the person's name:")
        if not person_name:
            messagebox.showinfo("Cancelled", "Dataset creation cancelled.")
            return

        # Ask for the number of images to capture
        try:
            num_images = int(simpledialog.askstring("Input", "Enter the number of images to capture:"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid number of images.")
            return

        # Create the dataset directory
        person_dir = os.path.join(dataset_dir, person_name)
        os.makedirs(person_dir, exist_ok=True)

        # Initialize the webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        messagebox.showinfo("Info", "Starting webcam. Press 'q' to quit early.")
        count = 0

        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture frame. Exiting...")
                break

            # Display the frame
            cv2.imshow(f"Capturing images for {person_name}", frame)

            # Save the frame as an image
            img_name = os.path.join(person_dir, f"{person_name}_{count + 1}.jpg")
            cv2.imwrite(img_name, frame)
            count += 1

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Info", f"Captured {count} images for {person_name}.")

    def face_rec(self):
        """Run the face recognition program."""
        program_path = r"C:\Users\varti\OneDrive\Desktop\project\smart_attendence_system_program.py"

        if not os.path.exists(program_path):
            messagebox.showerror("Error", f"Face recognition script not found:\n{program_path}")
            return

        try:
            subprocess.run(["python", program_path], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Face recognition failed:\n{e.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

    def open_attendance_sheet(self):
        """Open the attendance sheet Excel file."""
        try:
            if not os.path.exists(attendance_path):
                raise FileNotFoundError(f"Attendance sheet not found:\n{attendance_path}")
            os.startfile(attendance_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open attendance sheet:\n{e}")

    def open_intruder_log(self):
        """Open the intruder log Excel file."""
        try:
            if not os.path.exists(intruder_log_path):
                raise FileNotFoundError(f"Intruder log not found:\n{intruder_log_path}")
            os.startfile(intruder_log_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open intruder log:\n{e}")

    def Close(self):
        """Close the application with confirmation."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
