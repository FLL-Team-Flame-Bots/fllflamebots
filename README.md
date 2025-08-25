# Flame Bots FLL Team Code

Welcome to the official code repository for the Flame Bots FLL team! This repository contains all the Python code for our robot, designed to run on the LEGO SPIKE Prime Hub using Pybricks.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Step 1: Set up a GitHub Account](#step-1-set-up-a-github-account)
  - [Step 2: Clone the Repository](#step-2-clone-the-repository)
  - [Step 3: Read the Python Code](#step-3-read-the-python-code)
  - [Step 4: Upload and Run Code with Pybricks](#step-4-upload-and-run-code-with-pybricks)
- [Contributing](#contributing)

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine and on the robot hub for development and testing purposes.

### Prerequisites

*   A computer with an internet connection.
*   A web browser (like Chrome, Firefox, or Edge) that supports Web Bluetooth/Serial.
*   A LEGO SPIKE Prime Hub.
*   A USB cable to connect the hub to your computer.

### Step 1: Set up a GitHub Account

If you don't have a GitHub account, you'll need to create one to contribute to the project.

1.  Go to [https://github.com/join](https://github.com/join).
2.  Follow the on-screen instructions to create your free personal account.
3.  Install [GitHub Desktop](https://desktop.github.com/) application, which provides a graphical interface to interact with GitHub.
4.  (Optional for advanced users) [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on your computer and [configure it with your GitHub username and email](https://docs.github.com/en/get-started/getting-started-with-git/setting-your-username-in-git). This will allow you to use the command line for version control. 

### Step 2: Clone the Repository

"Cloning" the repository means creating a local copy of the project on your computer.

1.  Navigate to the main page of this repository on GitHub.
2.  Click the green `<> Code` button and select "Local" tab.
3.  Click "Open with GitHub Desktop". If prompted, allow your browser to open GitHub Desktop.
4.  In GitHub Desktop, confirm the repository details and click "Clone". Make sure you select a local folder on your computer to store the cloned repository.
5.  This will create a new folder named `fllflamebots` containing all the project files in your chosen local path.


### Step 3: Read the Python Code

Once you have the code on your computer, you can open the files in any text editor or IDE (like VS Code) to read and edit them.

Our project has a simple structure:

*   `unearthed/mainrobot.py`: This is the main entry point for our robot. It displays a menu on the hub's screen, allowing you to select which mission program to run.
*   `unearthed/sample_setup_run.py`: This is an example of a mission program. It demonstrates how to initialize Pybricks code with proper hub wiring, driving wheels, motors, and sensor settings, and contains a few examples of movements and actions for the robot to work on.

The code is written in Pybricks's block coding interface, and downloaded as Python files.

### Step 4: Upload and Run Code with Pybricks

To run the code on the robot, we use the Pybricks web interface.

1.  **Connect the Hub**: Turn on your LEGO Hub and connect it to your computer using Bluetooth.
2.  **Open Pybricks Code**: In a compatible web browser (like Google Chrome), go to https://code.pybricks.com/.
3.  **Connect to Hub in Pybricks**: Click the Bluetooth or USB icon in the Pybricks interface and follow the prompts to connect to your hub. Once connected, the hub will play a sound, and the icon will turn green.
4.  **Import and Run**:
    *   In the Pybricks editor, click the "File" menu, then "Import a file".
    *   Navigate to the `fllflamebots/unearthed` folder you cloned earlier.
    *   Select the Python file you want to import (e.g., `mainrobot.py`).
    *   After importing, you can run the file by clicking the "Run" button.

For more detailed instructions, please refer to the official Pybricks documentation.

## Contributing

We encourage all team members to contribute!

1.  Create new files in Pybricks web interface for your missions.
2.  Once working, download your files to `fllflamebots/unearthed` folder.
3.  Using Github Desktop app to add your files and commit. Each commit requires descriptions to help others understand what you have added/changed.
4.  Note that "commit" only happens on your own computer. The last step is to use Github Desktop to push your committed changes to Github server, thus all team members can see your latest changes.

---
Happy coding, and go Flame Bots! 🔥
