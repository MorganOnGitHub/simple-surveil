
# Simple Surveil

## Overview

The **Simple Surveil Camera Application** is a Python-based surveillance system that utilizes a webcam and the YOLO (You Only Look Once) object detection model to monitor specific objects in real-time. The application is capable of sending email notifications when the object of interest is detected and recording the event for later review. The application can be configured using environment variables and accepts command-line arguments to customize the behavior of the surveillance system.

## Features

- **Real-time Object Detection**: Uses YOLO model to detect specified objects (e.g., "person", "car", etc.) from webcam footage.
- **Email Notification**: Sends an email alert when the object of interest is detected.
- **Recording**: Starts recording when the object is detected, saving the video for later review.
- **Configurable Parameters**: The frame skip and recording duration can be customized via command-line arguments.
- **Environment Variable Configuration**: Sensitive information such as email credentials and SMTP settings are securely stored in a `.env` file.

## Requirements

To run the application, the following Python packages are required:

- `opencv-python` (for video capture and processing)
- `smtplib` (for sending email notifications)
- `threading` (for sending email notifications asynchronously)
- `ultralytics` (for YOLO object detection model)
- `python-dotenv` (for loading environment variables)

You can install the necessary packages using `pip`. To do so, download the `requirements.txt` file and run the following command:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Clone or Download the Repository

Clone the repository to your local machine.

### 2. Install Dependencies

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

Create a `.env` file in the root of the project directory with the following content. This file contains sensitive information such as email credentials and SMTP configuration:

```
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password
EMAIL_RECEIVER=receiver_email@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

Replace the placeholders with your actual email credentials and SMTP server details.

### 4. Model Setup

Ensure the YOLO model file (`yolo11l.pt`) is placed in the `models` directory. If not, download the appropriate model and place it in the `models` folder.

```
/models/yolo11l.pt
```

### 5. Run the Application

You can now run the security camera application using the following command:

```bash
python surveil.py
```

### Command-Line Arguments

You can pass the following command-line arguments to customize the behavior:

- `--surveil_object`: The object to monitor (default: `person`).
- `--frame_skip`: The number of frames to skip before performing object detection (default: `5`).
- `--record_duration`: The duration in seconds for which the application will record once the object is detected (default: `120`).
- `--model_path`: The path to the YOLO model file (default: `models/yolo11m.pt`).

#### Example:

```bash
python surveil.py --surveil_object person --frame_skip 10 --record_duration 180
```

This command will monitor for a "person" and skip every 10th frame before performing detection. The application will record for 180 seconds once a person is detected.

### 6. Exit the Application

To exit the application, press the `q` key in the video display window.

## Environment Variables

The application requires the following environment variables to be set in the `.env` file:

- `EMAIL_SENDER`: The email address used to send the notification.
- `EMAIL_PASSWORD`: The password for the email account.
- `EMAIL_RECEIVER`: The recipient's email address.
- `SMTP_SERVER`: The SMTP server address (e.g., `smtp.gmail.com`).
- `SMTP_PORT`: The SMTP server port (e.g., `587`).

## Example `.env` File

```
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password
EMAIL_RECEIVER=receiver_email@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

Ensure that the values in the `.env` file are correct and that your email account allows access for sending emails via SMTP (you may need to enable less secure app access for some email providers).

## Troubleshooting

1. **Model Not Found**: Ensure that the YOLO model file (`yolo11l.pt`) exists in the `models` directory. If not, download the correct model and place it in the directory.
2. **Webcam Not Detected**: Make sure your webcam is properly connected and accessible to OpenCV. Check if your camera drivers are up to date.
3. **Environment Variables Missing**: Make sure all necessary environment variables are set correctly in the `.env` file.

