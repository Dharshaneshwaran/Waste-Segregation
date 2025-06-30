import cv2
import numpy as np
import serial
import time
from PIL import Image, ImageTk, ImageOps
import tensorflow as tf
import tkinter as tk
from threading import Thread

# ===== Arduino Serial Port =====
arduino = serial.Serial('COM4', 9600)  # Change COM port if needed
time.sleep(2)

# ===== Load TFLite Model =====
interpreter = tf.lite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ===== Load Labels =====
with open("labels.txt", "r") as f:
    class_names = [line.strip().split(" ", 1)[1] for line in f.readlines()]

# ===== GUI Window =====
window = tk.Tk()
window.title("Waste Classifier AI")
window.geometry("700x600")
window.configure(bg="#f0f0f0")

# Webcam panel
video_label = tk.Label(window)
video_label.pack()

# Result label
result_var = tk.StringVar()
result_label = tk.Label(window, textvariable=result_var, font=("Arial", 16), bg="#f0f0f0", fg="black")
result_label.pack(pady=10)

# ===== Video Thread =====
cap = cv2.VideoCapture(0)

def video_loop():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Preprocess for model
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)
        image_resized = ImageOps.fit(image_pil, (224, 224), Image.Resampling.LANCZOS)
        image_array = np.asarray(image_resized).astype(np.float32)
        normalized_image_array = (image_array / 127.5) - 1.0
        input_data = np.expand_dims(normalized_image_array, axis=0)

        # Predict
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])[0]
        index = np.argmax(output_data)
        confidence = output_data[index]
        class_name = class_names[index]

        # Show result
        label_text = f"Detected: {class_name} ({confidence*100:.2f}%)"
        result_var.set(label_text)

        # Send to Arduino
        if index == 0:
            arduino.write(b'G')
        else:
            arduino.write(b'R')

        # Show on GUI
        image = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=image.resize((600, 400)))
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        time.sleep(0.1)

# Start video loop in thread
video_thread = Thread(target=video_loop, daemon=True)
video_thread.start()

# Start GUI loop
window.mainloop()

# Cleanup
cap.release()
arduino.close()
