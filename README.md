TAR UMT Assistant – Login & Registration System
Overview

This project is a Tkinter-based GUI application designed to handle user registration and login for the TAR UMT Assistant.
It allows students to create accounts with automatically generated student IDs, securely store credentials, and access the main application after login.

Features

-User Registration

  New users can register with a unique username and password.

  Automatically generates a 7-digit Student ID (e.g., 1000001).

  Prevents duplicate usernames.

  Displays success message with assigned ID.

-User Login

  Allows existing users to log in with their credentials.

  Displays assigned Student ID upon successful login.

  Redirects to the main application (homepage.open_main_app).

-User Management

  User accounts are stored in a CSV-style text file (data/users.txt).

  Supports both old format (username,password) and new format (student_id,username,password).

  Automatically creates the data/ directory and file if missing.

-GUI Design

  Built with Tkinter.

  Separate windows for Login and Register.

  Popup dialogs (messagebox) for feedback (success, error, warnings).

-Project Structure

  project_root/
  data/
  users.txt -> Stores registered users (auto-created if missing)
  homepage.py -> Contains open_main_app function (main app entry after login)
  login.py -> Main script (this file)
  README.txt -> Documentation

-How It Works

1.Registration Flow

  User clicks Register.

  Enters username and password.

  System checks for duplicates.

  Assigns a unique Student ID.

  Saves to users.txt.

  Shows success message.
 
2.Login Flow

  User enters username and password.

  System validates credentials.

  If correct → shows welcome message + ID, then opens main app.

  If incorrect → shows error popup.

-Example of users.txt

  1000001,tan,123
  1000002,lai,123
  1000003,low,123
  1000004,et,123
  1000005,jf,123




-How to Run

  Make sure you have Python 3.8+ installed.

  Run the login system:
  python login.py

  Use Register to create a new account.

  Use Login to enter the main app.





1.Simple Reminder System
-Overview

  This is a Tkinter-based GUI Reminder System that allows users to add, manage, and track reminders.
  Reminders are saved in CSV files per user and support repeat schedules (None, Daily, Weekly).
  The system also includes an alarm sound and popup notifications when the reminder time is reached.

-Features

  Add reminders with:

  Task description

  Date & Time (with AM/PM format)

  Repeat option (None, Daily, Weekly)

-Manage reminders:

  Refresh reminder list

  Delete selected reminders

  Cancel repeat reminders

  Clear all completed reminders (status "Rang")

-Alarm and notification:

  Plays beep sound when reminder time is reached

  Popup messagebox with reminder task

  Automatically creates next reminder if set to repeat

-Storage:

  Each user has their own CSV file (data/{username}_reminder.csv)

  File is auto-created if not present

  Reminders stored with fields: id, task, datetime, status, repeat

-Project Structure

  project_root/
  data/
  username_reminder.csv -> Reminder file for each user (auto-created)
  reminder.py -> Main reminder system (this file)
  README.txt -> Documentation

-Reminder Workflow

1.Add Reminder

  Enter task, date, time, and repeat option.

  Saved as "Pending" in user’s CSV file.

2.Alarm Trigger

  When reminder time is reached, status changes to "Ringing".

  Beep sound plays + popup alert message.

  Status then changes to "Rang".

3.Repeat Handling

  If set to Daily → new reminder added for next day.

  If set to Weekly → new reminder added for next week.

4.Managing Reminders

  "Refresh" → Reload list from CSV.

  "Delete Reminder" → Remove a specific reminder.

  "Cancel Repeat" → Stop repeat for selected reminder.

  "Clear All History" → Remove all reminders with status "Rang".

-Example of CSV file (user: testuser)

  id,task,datetime,status,repeat
  0,Submit Assignment,2025-09-20 09:00 AM,Pending,None
  1,Team Meeting,2025-09-21 02:30 PM,Rang,Daily
  2,Gym Workout,2025-09-22 07:00 PM,Pending,Weekly

-How to Run

  Ensure Python 3.8+ is installed.

  Run the reminder system from terminal or IDE:
  python reminder.py

  Use the interface to add, view, and manage reminders.








2.Student Timetable System
-Overview

  This project is a Tkinter-based GUI Student Timetable Application that allows users to create, view, and manage events such as classes, meetings, and personal tasks.
  The system supports event editing, deletion, appointment synchronization between two users, and integration with the reminder system.

-Features

1.Event Management

  Add new events with title, category, time, and description.

  Edit existing events (title, category, time, description).

  Delete events.
 
  Prevents overlapping (conflicting) events.

  Supports categories: event, class, meeting, appointment.

2.Appointment Synchronization

  If a user creates an appointment with another user, both users’ timetable files are updated.

  Deleting an appointment removes it from both users’ timetables.

3.Reminders

  Events can be toggled with a reminder option.

  Reminder system is linked to a separate CSV file (username_reminder.csv).

  Reminders integrate with the Simple Reminder module.

4.User Data Storage

  Each user has their own event CSV file (username_events.csv).

  Events are saved with:

  id, date, start_time, end_time, title, reminder, category, description

5.User Interface

  Filter events by category (all, event, class, appointment, meeting).

  Date selection via year, month, and day pickers.

  Table view with alternating row colors.

  Event details popup with description.

  Icons for edit and delete actions.

  Reminder checkbox for enabling/disabling event reminders.













3.Make Appointment System
-Overview

  This module is part of the Student Assistant System.
  It allows students to create and manage appointments with other registered users.
  Appointments are stored in each user’s timetable CSV file and checked for conflicts to prevent overlaps.

-Features

1.User Selection

  Loads all users from data/users.txt.

  Excludes the currently logged-in user.

  Supports both formats:

  username,password

  id,username,password

2.Appointment Creation

  Select another user, date, start time, and end time.

  Checks for:

  Valid date/time input

  Start time before end time

  Conflicts with current user’s timetable

  Conflicts with other user’s timetable

  Creates an appointment entry for both users:

  Current user → Appointment with <other user>

  Other user → Appointment with <current user>

3.Appointment Cancellation

  Select an appointment from history and cancel it.

  Deletes the appointment from both users’ timetables.

  Ensures data consistency between user files.

4.Appointment History

  Displays all appointments for the current user.

  Shows date, time (12-hour format), and title.

  Automatically refreshes after creation or cancellation.












4.Discussion Room Booking System
-Overview

  This is the main module of the Discussion Room Booking system.
  It serves as the dashboard and navigation hub for booking, checking availability, and managing user bookings.
  The GUI is built with Tkinter and ttk widgets for styling.

-Features

1.Dashboard

  Clean interface with three main actions:

  Book a Room

  View Availability

  My Bookings

  Back to Homepage button

2.Venue Selection

  Lists all available venues from rooms_data.py.
 
  Supports multiple venues (Library, Cyber Center, Faculty Blocks, Student Hub, Research Center).

  Color-coded buttons for each venue.

  Separate views for:

  Booking a room

  Viewing availability table

3.My Bookings Menu

  Organizes bookings into three categories:

  ⏳ Upcoming Bookings

  ❌ Cancelled Bookings

  📜 Past Bookings

  Each opens the respective page module (UpcomingBookings, CancelledBookings, PastBookings).

  Back button to return to the dashboard.

4.Page Dispatcher

  Central handler that loads different pages depending on user selection:

  Booking page → BookRoom.build_page()

  Availability page → ViewAvailability.build_page()

  My Bookings menu


-File Structure

  main.py – This file (MainApp class and navigation).

  BookRoom.py – Handles new room bookings.

  ViewAvailability.py – Shows available rooms by venue.

  UpcomingBookings.py – Lists upcoming reservations.

  CancelledBookings.py – Lists cancelled bookings.

  PastBookings.py – Lists completed bookings.

  rooms_data.py – Contains venue and room details.

-How It Works

  User logs in and opens the Discussion Room Booking dashboard.

  From the dashboard, they can:

  Book a new room by selecting a venue.

  Check room availability for upcoming days.

  View their personal bookings history.

  The system dynamically loads pages depending on user actions.
