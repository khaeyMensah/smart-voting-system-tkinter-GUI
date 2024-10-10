import tkinter as tk
import serial
from tkinter import filedialog, messagebox, scrolledtext
import csv
import time

# Tkinter setup
root = tk.Tk()
root.title("Voting Control Panel")
root.geometry("1000x600")  # Adjusted size to accommodate sidebars and main section

voter_database = None
searched_index = None
votes_visible = False  # To toggle view/hide votes
pc_timeout_occurred = False  # Track if a timeout has occurred


# Set up serial communication with CP2102
try:
    ser = serial.Serial('COM7', 9600, timeout=2)  # Adjust COM port as needed
    time.sleep(2)  # Allow some time for serial connection to establish
except serial.SerialException:
    ser = None  # Handle case where Arduino is not connected
    messagebox.showwarning("Warning", "Arduino not connected. Running in mock mode.")

# Function to upload CSV file
def upload_csv():
    global voter_database
    voter_database = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV Files", "*.csv"),))
    if voter_database:
        upload_status_label.config(text=f"Database Uploaded: {voter_database.split('/')[-1]}", fg="green")
    else:
        upload_status_label.config(text="No CSV uploaded.", fg="red")

# Function to search for a voter's details by index number
def search_voter():
    global searched_index
    index_number = index_entry.get()  # Get the entered index number
    if voter_database and index_number:
        with open(voter_database, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[4] == index_number:  # Assuming index number is in the 5th column
                    name, department, program, level = row[3], row[0], row[1], row[2]
                    voter_details_label.config(text=f"Name: {name}\nDepartment: {department}\nProgram: {program}\nLevel: {level}\nIndex: {index_number}", fg="green")

                    # Send query to Arduino to check if the voter has already voted
                    if ser:
                        ser.write(f"HAS_VOTED {index_number}\n".encode())
                        time.sleep(2)
                        arduino_response = ser.readline().decode('utf-8').strip()
                        if arduino_response == "VOTER_VOTED":
                            result_label.config(text="Voter has already voted.", fg="red")
                            confirm_button.config(state=tk.DISABLED)  # Disable confirm button if already voted
                        else:
                            result_label.config(text="Voter found!", fg="green")
                            confirm_button.config(state=tk.NORMAL)  # Enable confirm button if eligible
                    else:
                        result_label.config(text="Voter found!", fg="green")

                    searched_index = index_number  # Store the searched index number
                    log_messages.insert(tk.END, f"Voter {index_number} found.\n")
                    return
            result_label.config(text="Voter not found.", fg="red")
            log_messages.insert(tk.END, f"Voter {index_number} not found.\n")
    else:
        result_label.config(text="Please upload a CSV file and enter an index number.", fg="red")


# Function to confirm voter eligibility
def confirm_voter():
    global searched_index
    if searched_index:
        index_number = searched_index  # Get the last searched index number
        if ser:
            ser.write(f"CONFIRM_VOTER {index_number}\n".encode())  # Send confirmation command to Arduino

            time.sleep(2)  # Wait for Arduino to respond
            if ser.in_waiting > 0:  # Check for response
                arduino_response = ser.readline().decode('utf-8').strip()

                if arduino_response == "VOTER_CONFIRMED":
                    log_messages.insert(tk.END, f"Voter {searched_index} confirmed.\n")
                    result_label.config(text="Voter confirmed. Proceed to voting.", fg="green")
                    confirm_button.config(state=tk.DISABLED)  # Disable confirm button after confirmation

                elif arduino_response == "VOTER_ERROR":
                    result_label.config(text="Error: Voter not found or already voted.", fg="red")
            else:
                result_label.config(text="No response from Arduino system.", fg="orange")
        else:
            result_label.config(text="Arduino not connected.", fg="red")
    else:
        result_label.config(text="Please search for a voter first.", fg="red")


# def confirm_voter():
#     global searched_index
#     if searched_index:
#         index_number = searched_index  # Get the last searched index number
#         if ser:
#             ser.write(f"CONFIRM_VOTER {index_number}\n".encode())

#             time.sleep(2)  # Wait for Arduino to respond
#             if ser.in_waiting > 0:  # Check for response
#                 arduino_response = ser.readline().decode('utf-8').strip()

#                 if arduino_response == "VOTER_CONFIRMED":
#                     log_messages.insert(tk.END, f"Voter {searched_index} confirmed.\n")
#                     result_label.config(text="Voter confirmed. Proceed to voting.", fg="green")
#                 elif arduino_response == "VOTER_ERROR":
#                     result_label.config(text="Error: Voter not found in system.", fg="red")
#             else:
#                 result_label.config(text="No response from Arduino system.", fg="orange")
#         else:
#             result_label.config(text="Arduino not connected.", fg="red")
#     else:
#         result_label.config(text="Please search for a voter first.", fg="red")


# # Function to confirm voter and send command to Arduino
# def confirm_voter():
#     global searched_index
#     if searched_index:
#         index_number = searched_index  # Get the last searched index number
#         if ser:
#             ser.write(f"CONFIRM_VOTER {index_number}\n".encode())  # Send confirmation command to Arduino
#             print(f"Debug: Sent CONFIRM_VOTER {index_number} to Arduino")  # Debugging message

#             # Wait for Arduino response (increased wait time for better syncing)
#             time.sleep(2)  # Give more time for Arduino to process
#             if ser.in_waiting > 0:  # Check if there's any data waiting in the buffer
#                 arduino_response = ser.readline().decode('utf-8').strip()
#                 print(f"Debug: Arduino Response: {arduino_response}")  # Debugging message

#                 if arduino_response == "VOTER_CONFIRMED":
#                     log_messages.insert(tk.END, f"Voter {searched_index} confirmed.\n")
#                     result_label.config(text="Voter confirmed. Proceed to voting.", fg="green")
#                 elif arduino_response == "VOTER_ERROR":
#                     log_messages.insert(tk.END, f"Voter {searched_index} not found in system.\n")
#                     result_label.config(text="Error: Voter not found in Arduino system.", fg="red")
#             else:
#                 log_messages.insert(tk.END, f"No response from Arduino system for voter {searched_index}.\n")
#                 result_label.config(text="No response from Arduino system.", fg="orange")
#         else:
#             print("Debug: Arduino not connected, mock response used")  # Debugging message
#             log_messages.insert(tk.END, f"Voter {searched_index} confirmed (mock mode).\n")
#             result_label.config(text="Voter confirmed (mock mode).", fg="green")
#     else:
#         result_label.config(text="Please search for a voter first.", fg="red")
#         log_messages.insert(tk.END, "Attempted to confirm voter without a search.\n")
#         print("Debug: No voter searched yet")  # Debugging message


# # Function to confirm voter and send command to Arduino
# def confirm_voter():
#     global searched_index
#     if searched_index:
#         index_number = searched_index  # Get the last searched index number
#         if ser:
#             ser.write(f"CONFIRM_VOTER {index_number}\n".encode())  # Send confirmation command to Arduino
#             print(f"Debug: Sent CONFIRM_VOTER {index_number} to Arduino")  # Debugging message

#             # Wait for Arduino response (increased wait time for better syncing)
#             time.sleep(2)  # Give more time for Arduino to process
#             if ser.in_waiting > 0:  # Check if there's any data waiting in the buffer
#                 arduino_response = ser.readline().decode('utf-8').strip()
#                 print(f"Debug: Arduino Response: {arduino_response}")  # Debugging message

#                 if arduino_response == "VOTER_CONFIRMED":
#                     log_messages.insert(tk.END, f"Voter {searched_index} confirmed.\n")
#                     result_label.config(text="Voter confirmed. Proceed to voting.", fg="green")
#                 elif arduino_response == "VOTER_ERROR":
#                     result_label.config(text="Error: Voter not found in Arduino system.", fg="red")
#                 else:
#                     result_label.config(text="Unexpected response from Arduino system.", fg="orange")
#             else:
#                 print("Debug: No response from Arduino system")  # Debugging message
#                 result_label.config(text="No response from Arduino system.", fg="orange")
#         else:
#             print("Debug: Arduino not connected, mock response used")  # Debugging message
#             log_messages.insert(tk.END, f"Voter {searched_index} confirmed (mock mode).\n")
#             result_label.config(text="Voter confirmed (mock mode).", fg="green")
#     else:
#         result_label.config(text="Please search for a voter first.", fg="red")
#         log_messages.insert(tk.END, "Attempted to confirm voter without a search.\n")
#         print("Debug: No voter searched yet")  # Debugging message

# # Function to reject voter
# def reject_voter():
#     global searched_index
#     if searched_index:
#         ser.write(f"REJECT_VOTER {searched_index}\n".encode())  # Send rejection command to Arduino
#         log_messages.insert(tk.END, f"Voter {searched_index} rejected.\n")
#         result_label.config(text="Voter rejected.", fg="red")
#     else:
#         result_label.config(text="Please search for a voter first.", fg="red")

# Function to toggle between view and hide votes
def toggle_votes():
    global votes_visible
    if votes_visible:
        votes_visible = False
        view_votes_button.config(text="View Votes")
        vote_sidebar.config(state=tk.NORMAL)
        vote_sidebar.delete('1.0', tk.END)  # Clear vote counts
        vote_sidebar.config(state=tk.DISABLED)
    else:
        votes_visible = True
        view_votes_button.config(text="Hide Votes")
        vote_sidebar.config(state=tk.NORMAL)
        if ser:
            ser.write(b'VIEW_VOTES\n')  # Send the command to Arduino to view votes
            arduino_response = ser.readlines()  # Read all lines sent by Arduino
            vote_display = ""  # String to hold the vote display information
            for line in arduino_response:
                line = line.decode('utf-8').strip()
                if line:
                    vote_display += line + "\n"  # Append each line of vote count information
            vote_sidebar.insert(tk.END, vote_display)
        else:
            vote_sidebar.insert(tk.END, "Votes:\nCandidate 1: 10\nCandidate 2: 15\nCandidate 3: 5\n")  # Example mock vote counts
        vote_sidebar.config(state=tk.DISABLED)

# Function to send a start command
def start_voting():
    ser.write(b'START_VOTE\n')
    log_messages.insert(tk.END, "Voting started.\n")

# Function to send an end command
def end_voting():
    ser.write(b'END_VOTE\n')
    log_messages.insert(tk.END, "Voting ended.\n")

# Function to handle "PC Timeout" and enable the button
def handle_timeout():
    global pc_timeout_occurred
    pc_timeout_occurred = True
    online_button.config(state=tk.NORMAL)  # Enable the online button
    log_messages.insert(tk.END, "PC timeout detected. Please indicate PC is back online.\n")


# Function to send an "ONLINE" command to the Arduino
def indicate_online():
    global pc_timeout_occurred  # Declare 'global' at the top before using the variable
    if ser and pc_timeout_occurred:
        ser.write(b'ONLINE\n')
        log_messages.insert(tk.END, "PC is back online.\n")
        online_button.config(state=tk.DISABLED)  # Disable button again
        pc_timeout_occurred = False


# Function to read logs from Arduino
def read_logs():
    if ser:
        while ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if "PC timeout" in data:
                handle_timeout()  # Detect and handle PC timeout
            log_messages.insert(tk.END, f"{data}\n")

# Function to close the serial port and exit the app
def on_closing():
    if ser:
        ser.close()  # Close the serial port if it's open
    root.destroy()  # Close the GUI window

# Variables for log display
log_messages = tk.StringVar()
log_messages.set("Voting Logs:\n")

# Layout Components

# Create a PanedWindow for adjustable side panels
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=1)


# Left Frame for votes (adjustable)
left_frame = tk.Frame(paned_window, width=200, bg='lightgray')
paned_window.add(left_frame, minsize=200)  # Add left panel to paned window

# Main Frame in the middle (adjustable)
main_frame = tk.Frame(paned_window, bg='white')
paned_window.add(main_frame, minsize=500)  # Add main panel to paned window

# Right Frame for logs (adjustable)
right_frame = tk.Frame(paned_window, width=200, bg='lightgray')
paned_window.add(right_frame, minsize=200)  # Add right panel to paned window

# Start Button
start_button = tk.Button(main_frame, text="Start Voting", command=start_voting)
start_button.pack(pady=10)

# End Button
end_button = tk.Button(main_frame, text="End Voting", command=end_voting)
end_button.pack(pady=10)

# Upload CSV button
upload_button = tk.Button(main_frame, text="Upload CSV", command=upload_csv)
upload_button.pack(pady=10)

upload_status_label = tk.Label(main_frame, text="No CSV uploaded.")
upload_status_label.pack(pady=5)

# Index Number Label and Entry
index_label = tk.Label(main_frame, text="Enter Voter's Index Number:")
index_label.pack(pady=10)

index_entry = tk.Entry(main_frame)
index_entry.pack(pady=5)

# Search Button
search_button = tk.Button(main_frame, text="Search Voter", command=search_voter)
search_button.pack(pady=10)

# Voter Details Label
voter_details_label = tk.Label(main_frame, text="Voter details will appear here.", justify="left")
voter_details_label.pack(pady=10)

# Confirm Button
confirm_button = tk.Button(main_frame, text="Confirm Voter", command=confirm_voter)
confirm_button.pack(pady=10)

# Online Button (blurred initially, enabled on PC timeout)
online_button = tk.Button(main_frame, text="Indicate PC Online", command=indicate_online, state=tk.DISABLED)
online_button.pack(pady=10)

# View Votes Button
view_votes_button = tk.Button(left_frame, text="View Votes", command=toggle_votes)
view_votes_button.pack(pady=10)

# Result Label (to show success or error messages)
result_label = tk.Label(main_frame, text="", fg="red")
result_label.pack(pady=5)

# Vote Sidebar for displaying vote counts (left side)
vote_sidebar = scrolledtext.ScrolledText(left_frame, width=25, height=30, bg='lightgray', state=tk.DISABLED)
vote_sidebar.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Log Label
log_label = tk.Label(right_frame, text="Log Messages", justify="left")
log_label.pack(pady=10)

# Log Sidebar for displaying logs (right side)
log_messages = scrolledtext.ScrolledText(right_frame, width=25, height=30, bg='lightgray')
log_messages.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Exit button
exit_button = tk.Button(main_frame, text="Exit", command=on_closing)
exit_button.pack(pady=10)

# Periodically read logs
def periodic_read_logs():
    read_logs()
    root.after(1000, periodic_read_logs)

root.after(1000, periodic_read_logs)

# Start the Tkinter loop
root.protocol("WM_DELETE_WINDOW", on_closing)  # Ensure the serial port is closed when the window is closed
root.mainloop()
