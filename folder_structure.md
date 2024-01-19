### File structure

For ChatGPT prompts

```
fov-cameras-web-app
├─ .gitignore
├─ .vscode
│  └─ settings.json
├─ client
│  ├─ .env
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  ├─ favicon.ico
│  │  ├─ index.html
│  │  ├─ logo192.png
│  │  ├─ logo512.png
│  │  ├─ manifest.json
│  │  └─ robots.txt
│  ├─ README.md
│  └─ src
│     ├─ components
│     │  ├─ App.js
│     │  ├─ firebase.js
│     │  ├─ Login.js
│     │  ├─ MotorControlForm.js
│     │  ├─ MotorPositions.js
│     │  ├─ ServerImage.js
│     │  ├─ StartStopCameraControl.js
│     │  ├─ StartStopCameraStream.js
│     │  ├─ StatusList.js
│     │  ├─ useAuth.js
│     │  ├─ useSendCommand.js
│     │  └─ useStatus.js
│     ├─ index.js
│     └─ stylesheets
│        ├─ App.css
│        ├─ MotorPositions.css
│        └─ StatusList.css
├─ flowcharts
│  └─ flowchart.drawio
├─ jetson
|  ├─ .env
│  ├─ camera_control_pid.txt
│  ├─ ip_address.txt
│  ├─ jetson_stream_simulator.py
│  ├─ learning
│  │  ├─ hello_world.py
│  │  ├─ number_input_loop.py
│  │  └─ while_hello_world.py
│  ├─ nano_requirements.txt
│  └─ stepperTests.py
├─ README.md
└─ server
   ├─ .env
   ├─ .dockerignore
   ├─ .ebextensions
   │  └─ python.config
   ├─ .gitignore
   ├─ app.zip
   ├─ application.py
   ├─ application_old.py
   ├─ Dockerfile
   ├─ notes.md
   ├─ Procfile
   ├─ requirements.txt
   ├─ server.py
   ├─ stream_manager.py
   └─ __pycache__
```
