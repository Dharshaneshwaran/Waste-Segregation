
# ♻️ Waste Classifier AI with Arduino UNO

This project uses a **Teachable Machine-trained TensorFlow Lite model** to classify waste as **biodegradable** or **non-biodegradable** in real-time using a webcam. Based on the prediction, an Arduino UNO blinks:

- 🟢 Green LED → Biodegradable
- 🔴 Red LED → Non-Biodegradable

---

## 📦 Features

- Real-time waste detection via webcam
- TensorFlow Lite `.tflite` model (from Teachable Machine)
- Python GUI using Tkinter
- LED control via Arduino UNO and serial communication
- Simple and educational for school projects

---

## 🛠️ Requirements

### Python (install with pip)

```bash
pip install tensorflow opencv-python pillow pyserial
````

### Arduino Circuit

| LED Color | Arduino Pin | Components         |
| --------- | ----------- | ------------------ |
| Green     | 9           | 220Ω resistor, GND |
| Red       | 10          | 220Ω resistor, GND |

---

## 📁 File Structure

```
project/
│
├── model_unquant.tflite       # Teachable Machine model
├── labels.txt                 # Labels from Teachable Machine
├── main_gui.py                # Python script with GUI
├── arduino_waste_led.ino      # Arduino sketch
└── README.md                  # This file
```

---

## 🚀 How to Run

### 1. Train a Model

* Go to [Teachable Machine](https://teachablemachine.withgoogle.com/)
* Train an **image classification model** with 2 classes
* Export as **TensorFlow Lite → Floating Point**
* Save the `.tflite` model and `labels.txt`

### 2. Upload to Arduino

Upload this code using Arduino IDE:

```cpp
#define GREEN_LED 9
#define RED_LED 10

void setup() {
  Serial.begin(9600);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    char signal = Serial.read();

    if (signal == 'G') {
      digitalWrite(GREEN_LED, HIGH);
      delay(500);
      digitalWrite(GREEN_LED, LOW);
    }
    else if (signal == 'R') {
      digitalWrite(RED_LED, HIGH);
      delay(500);
      digitalWrite(RED_LED, LOW);
    }
  }
}
```

### 3. Run the Python Script

```bash
python main.py
```

* A GUI window opens with your webcam feed
* Waste is classified live
* LEDs blink accordingly (green or red)

---

## 🧠 Notes

* Update `"COM3"` in the Python script if your Arduino uses a different port
* `Class 1` is treated as **biodegradable**, `Class 2` as **non-biodegradable**
* You can rename the entries in `labels.txt` to make them more readable

---

## 📄 License

MIT License – feel free to modify or use this in educational projects.


