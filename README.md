# Dronve Vision Control v1.0

## Getting Started

To setup this project, follow these steps:

### 1. Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/rifolio/ComputerVision-DroneControl.git
```

### 2. Set Up Virtual Environment

Navigate to the project directory and set up a virtual environment by running:

```bash
python3.9 -m venv drone #make sure to use python3.9
```

### 3. Activate Virtual Environment

Activate the virtual environment using:

```bash
source drone/bin/activate
```

### 4. Install Dependencies

Install the project dependencies using pip:

```bash
pip3 install -r requirements.txt
```

The `requirements.txt` file contains the following packages:

```
djitellopy
mediapipe
opencv-python
djitellopy
```

### 5. Set up Tello Drone

1. Activate your drone using mobile app (for the frist time)
2. Try connecting to drone's wifi and running: 
```bash
tello = Tello()
tello.connect()
```

You should receive something like this: 
```bash
[INFO] tello.py - 438 - Send command: 'command'
[INFO] tello.py - 462 - Response command: 'ok'
```

### 6. Run main.py

```bash 
python3 main.py
````
