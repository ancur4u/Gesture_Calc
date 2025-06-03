how to:
🧠 How to Run the Gesture-Controlled Calculator

This guide explains how to set up and run the Gesture-Controlled Virtual Calculator project built using Python, OpenCV, and MediaPipe.

⸻

📋 Prerequisites
	•	macOS or Windows/Linux
	•	Python 3.10
	•	Git
	•	A webcam (built-in or external)

⸻

🛠️ Setup Instructions

1. 🔁 Clone the Repository
git clone https://github.com/your-username/gesture-calculator.git
cd gesture-calculator

2. 🐍 Create Python 3.10 Virtual Environment
# If you use pyenv (recommended)
pyenv install 3.10.13
pyenv virtualenv 3.10.13 gesture_env
pyenv activate gesture_env

# Or using venv
python3.10 -m venv gesture_env
source gesture_env/bin/activate  # On Windows use: gesture_env\Scripts\activate

3. 📦 Install Requirements

Update pip and install dependencies:
pip install --upgrade pip
pip install opencv-python mediapipe==0.10.14
⚠️ mediapipe==0.10.14 requires protobuf>=4.25.3 which may conflict with older versions of Streamlit. Avoid using Streamlit for the OpenCV version.

🚀 Run the App
python app.py

	•	Press s or wait 5 seconds to start detecting gestures.
	•	Use your index finger to hover over calculator buttons.
	•	The selection is made after hovering for 0.5 seconds.
	•	Press q to quit the application.

🧪 Features
	•	Full expression support: +, -, *, /, =, ., ()
	•	ANS button to recall last result
	•	BCK (Backspace) & CLR (Clear)
	•	Hover animations and delay to avoid false triggers

📺 Demo Video

Watch the calculator in action:
📹 https://youtu.be/_oAgDJl4avA


🙋 Common Issues

❌ ModuleNotFoundError: No module named 'mediapipe'

Make sure you’re using Python 3.10+ and installed mediapipe with:
pip install mediapipe==0.10.14

❌ cv2.error: The function is not implemented
On Linux, install missing video codecs:
sudo apt-get install libopencv-dev python3-opencv ffmpeg
