# smart-voting-system-tkinter-GUI

# Smart Voting System with Interactive Input Capture

This project is a **final-year project** developed by a group of students to build a **Smart Voting System** with a focus on security, efficiency, and interactive input capture using a **Tkinter-based Python application** and **Arduino** hardware components.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [System Components](#system-components)
- [Architecture Overview](#architecture-overview)
- [Arduino Components](#arduino-components)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)

## Introduction

The **Smart Voting System** integrates hardware components with an interactive graphical user interface (GUI) to allow secure, real-time voting. The system focuses on:

- **Preventing multiple votes** by the same user.
- **Real-time communication** between the GUI and the Arduino using serial communication (via CP2102).
- **Efficient logging** of votes and voters.
- **Verification of voters** through an online or offline process.

## Features

- **Tkinter GUI for Voter Management:**
  - Search for voter details using an index number.
  - Display voter details, including name, department, program, and level.
  - Confirm voter eligibility.
  - Display verification status (whether the voter has voted).
  - Disable the confirm button for ineligible voters (voters who have already voted).
- **Real-Time Voting System**:
  - Voting process is controlled through an Arduino with hardware input buttons.
  - Votes are logged securely in CSV format.
  - The system prevents voters from voting more than once.
- **Arduino Communication**:
  - The Tkinter app communicates with the Arduino via serial communication (CP2102) for voter verification and vote logging.
  - The system runs locally when no PC is connected and handles voting independently.

## System Components

The **Smart Voting System** consists of both hardware and software components:

1. **Software**:
   - **Python** (Tkinter for GUI)
   - **Arduino IDE** (for Arduino code)
   - **CSV File Handling** (for managing voter data and vote logs)
2. **Hardware**:
   - **Arduino Mega** (to control voting input and output)
   - **CP2102 USB to Serial** (for communication between the Python app and Arduino)
   - **TFT Display** (for interactive display)
   - **Push buttons** (for selecting candidates and casting votes)
   - **Buzzer** (for auditory feedback on voting completion or errors)
   - **LEDs** (to indicate system status like power and error)
   - **SD Card Module** (for storing voter and vote data)

## Architecture Overview

The system has two primary components:

1. **Tkinter Voting Management GUI**:
   - A Python app that handles voter search, confirmation, and voter status check (whether they have already voted).
   - When connected to the Arduino, the GUI sends commands to verify and confirm voters. It ensures no duplicate votes are cast by disabling voting for already-voted users.
2. **Arduino Voting Controller**:
   - The Arduino manages the voting process using hardware buttons and a TFT display.
   - It handles the voting screen, logs votes to a CSV file, and provides feedback through LEDs and buzzers.
   - It runs independently when the PC is disconnected, verifying voters locally via SD card.

## Arduino Components

- **Arduino Mega**: The microcontroller responsible for controlling the voting process.
- **CP2102 USB to Serial Module**: Handles communication between the PC (Tkinter app) and Arduino.
- **Push Buttons**: Allow voters to select candidates and confirm votes.
- **TFT Display**: Displays voting details and progress.
- **Buzzer and LEDs**: Provide feedback to voters during the process.
- **SD Card Module**: Used to store voting logs, voter data, and results.

## Installation

### Requirements:

- **Python 3.7+**
- **Tkinter**: This comes pre-installed with Python but can be installed using:
  ```bash
  sudo apt-get install python3-tk
  ```
- **Arduino IDE**: For uploading code to the Arduino Mega.
- **CP2102 Drivers**: Install drivers to enable serial communication between PC and Arduino.
- **Libraries**: Ensure you have the following Python libraries:

```bash
pip install pyserial
```

## Steps:

1. **Clone the Repository**:

```bash
git clone https://github.com/yourusername/smart-voting-system.git
cd smart-voting-system
```

2. **Run the Tkinter App**:

```bash
python svs_control.py
```

3. **Upload the Arduino Code**: Open the arduino_voting_system.ino file in the Arduino IDE, and upload it to the **Arduino Mega** board.
4. **Connect the Hardware**:
   - Connect the **Arduino Mega** and **CP2102** to the PC.
   - Ensure all push buttons, LEDs, TFT display, and SD card modules are connected as per the provided circuit design.

## Usage

1. **Start the Tkinter Application**: The GUI will allow you to:

   - Upload the CSV file containing voter details.
   - Search for a voter by entering the index number.
   - Confirm voter eligibility based on whether they have already voted.

2. **Voter Verification**:

   - When connected to the Arduino, the GUI verifies the voter's status via serial communication.
   - If the voter has already voted, the Confirm button will be disabled, preventing them from voting again.

3. **Voting Process**:

   - After confirmation, the Arduino allows the voter to cast their vote using the push buttons.
   - The vote is logged, and the voter's index number is stored to prevent multiple votes.

4. **View Votes**: You can request vote counts from the Arduino using the View Votes button in the Tkinter app.

## Screenshots

[Tkinter GUI](/tkinter-gui.jpg)

## Future Enhancements

- **Multi-language support**: Expand the system to support multiple languages for a more inclusive experience.
- **Enhanced Security**: Incorporate biometric or facial recognition for stronger voter verification.
- **Mobile App**: Develop a mobile app to allow remote voting under secure conditions.
