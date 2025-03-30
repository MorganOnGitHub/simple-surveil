import cv2
import time
import os
import smtplib
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from ultralytics import YOLO

# Load environment variables
load_dotenv()

def validate_env_variables():
    # Get the environment variables from .env
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")

    # Check if any of the required environment variables are not set
    required_vars = [
        ("EMAIL_SENDER", EMAIL_SENDER),
        ("EMAIL_PASSWORD", EMAIL_PASSWORD),
        ("EMAIL_RECEIVER", EMAIL_RECEIVER),
        ("SMTP_SERVER", SMTP_SERVER),
        ("SMTP_PORT", SMTP_PORT)
    ]

    for var_name, var_value in required_vars:
        if var_value is None or (isinstance(var_value, str) and not var_value.strip()):
            print(f"Error: {var_name} is not set in the .env file or is empty!")
            exit()

    # Validate SMTP_PORT is a valid integer
    try:
        smtp_port = int(SMTP_PORT)  # This will raise ValueError if SMTP_PORT is not a valid integer
    except ValueError:
        print("Error: SMTP_PORT is not a valid integer!")
        exit()

validate_env_variables()

class SurveillanceSystem:
    def __init__(self, surveil_object="person", model_path="models/yolo11l.pt", frame_skip=5, record_duration=120):
        self.surveil_object = surveil_object.lower()
        self.model_path = model_path
        self.frame_skip = frame_skip  # Frame skipping value
        self.record_duration = record_duration  # Duration of recording in seconds

        os.makedirs("models", exist_ok=True)

        # Validate the model path
        if not os.path.exists(self.model_path):
            print(f"Error: Model file '{self.model_path}' not found. Ensure the model is in the 'models' directory.")
            exit()

        # Load YOLO model
        try:
            self.model = YOLO(self.model_path)
            print(f"Model '{self.model_path}' loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            exit()

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        # Set webcam resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Create recordings directory
        self.recording_dir = "recordings"
        os.makedirs(self.recording_dir, exist_ok=True)

        # Recording attributes
        self.video_writer = None
        self.recording = False
        self.start_time = None
        self.email_sent = False
        self.frame_count = 0

    def send_email_notification(self):
        """Send an email notification when the object is detected."""
        try:
            subject = f"{self.surveil_object.capitalize()} Detected Alert!"
            body = f"A {self.surveil_object} was detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

            msg = MIMEMultipart()
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Send email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            server.quit()

            print("Email notification sent successfully.")

        except Exception as e:
            print(f"Error sending email: {e}")

    def send_email_notification_async(self):
        """Send email asynchronously to avoid blocking execution."""
        email_thread = threading.Thread(target=self.send_email_notification)
        email_thread.start()

    def start_surveillance(self):
        """Start real-time surveillance."""
        print(f"Monitoring for '{self.surveil_object}'... Press 'q' to exit.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            self.frame_count += 1
            detected = False

            if self.frame_count % self.frame_skip == 0:
                # Resize frame to improve performance
                frame_resized = cv2.resize(frame, (640, 480))

                # Perform object detection
                results = self.model(frame_resized)
                detected_classes = results[0].names
                detections = results[0].boxes

                # Check if the specified object is detected
                for box in detections:
                    class_id = int(box.cls[0])
                    class_name = detected_classes[class_id]
                    if class_name.lower() == self.surveil_object:
                        detected = True
                        break  # No need to check further

                if detected:
                    print(f"{self.surveil_object.upper()} DETECTED!")

                    # Send email notification asynchronously
                    if not self.email_sent:
                        self.send_email_notification_async()
                        self.email_sent = True  # Prevent duplicate emails

                    # Start recording if not already recording
                    if not self.recording:
                        self.recording = True
                        self.start_time = time.time()
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        video_filename = os.path.join(self.recording_dir, f"detected_{self.surveil_object}_{timestamp}.mp4")

                        # Define video codec and create VideoWriter
                        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                        self.video_writer = cv2.VideoWriter(video_filename, fourcc, 30.0, (frame.shape[1], frame.shape[0]))

                        print(f"Recording started... Saving as {video_filename}")

                else:
                    self.email_sent = False  # Reset email flag

                # Write frames to video if recording
                if self.recording and self.video_writer:
                    self.video_writer.write(frame)

                    # Stop recording after specified duration
                    if time.time() - self.start_time >= self.record_duration:
                        self.recording = False
                        self.video_writer.release()
                        self.video_writer = None
                        print(f"Recording saved in '{self.recording_dir}'.")

            # Display the detection results
            annotated_frame = results[0].plot() if detected else frame
            cv2.imshow("Simple Surveil", annotated_frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Cleanup
        self.cap.release()
        if self.video_writer:
            self.video_writer.release()
        cv2.destroyAllWindows()
