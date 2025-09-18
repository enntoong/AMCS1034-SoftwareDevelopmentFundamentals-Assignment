# File: room_booking/UpcomingBookings.py

import tkinter as tk                                # Import tkinter for GUI
from tkinter import ttk, messagebox                 # Import ttk for modern widgets, messagebox for dialogs
import os, csv, datetime as dt                      # Import os (file paths), csv (read/write), datetime (time handling)
from .BookRoom import fetch_upcoming_bookings       # Import function to fetch upcoming bookings
from .helpers import user_in_booking                # Import helper to check if user is in a booking

# File paths
BOOKINGS_FILE = os.path.join("data", "bookings.csv")        # Path for active bookings
CANCELLED_FILE = os.path.join("data", "cancelled_bookings.csv")  # Path for cancelled bookings


def move_to_cancelled(booking: dict):  # Function to move booking from active list to cancelled list
    """Move booking to cancelled file and remove from active bookings"""
    if not os.path.exists(CANCELLED_FILE):  # If cancelled file doesn’t exist, create it with headers
        with open(CANCELLED_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=booking.keys())  # Use same fields as booking dict
            writer.writeheader()

    # Append this booking into cancelled file
    with open(CANCELLED_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=booking.keys())
        writer.writerow(booking)

    # Remove booking from active bookings file
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:  # Read all current bookings
            rows = list(csv.DictReader(f))
        # Keep only those bookings that are not the cancelled one
        rows = [r for r in rows if not (
            r["venue"] == booking["venue"]
            and r["room"] == booking["room"]
            and r["date"] == booking["date"]
            and r["start"] == booking["start"]
            and r["end"] == booking["end"]
            and r["owner_id"] == booking["owner_id"]
        )]
        # Write remaining bookings back to file
        with open(BOOKINGS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=booking.keys())
            writer.writeheader()
            writer.writerows(rows)


def build_page(parent, current_user, back_callback=None):  # Function to build Upcoming Bookings page
    for w in parent.winfo_children():   # Clear all child widgets
        w.destroy()

    now = dt.datetime.now()             # Current date and time
    today = now.date()                  # Current date only

    # ===== Header =====
    title_frame = ttk.Frame(parent)     # Header frame
    title_frame.pack(fill="x", pady=10) # Place at top

    # Page title
    ttk.Label(
        title_frame, text="📅 My Upcoming Bookings",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=10)

    # Buttons frame on the right (refresh + back)
    btn_frame = ttk.Frame(title_frame)
    btn_frame.pack(side="right")

    # Refresh button → reloads this page
    ttk.Button(
        btn_frame, text="🔄 Refresh", width=10,
        command=lambda: build_page(parent, current_user, back_callback)
    ).pack(side="left", padx=5)

    # Back button → return to previous page
    ttk.Button(
        btn_frame, text="⬅ Back", width=10,
        command=(lambda: back_callback()) if back_callback else None
    ).pack(side="left", padx=5)

    # ===== Scrollable area =====
    canvas = tk.Canvas(parent)                             # Canvas for scrolling
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)  # Vertical scrollbar
    scroll_frame = ttk.Frame(canvas, padding=10)           # Inner frame with padding
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  # Update scrollable area
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")  # Place frame in canvas
    canvas.configure(yscrollcommand=scrollbar.set)         # Connect scrollbar
    canvas.pack(side="left", fill="both", expand=True)     # Pack canvas
    scrollbar.pack(side="right", fill="y")                 # Pack scrollbar

    # ===== Data =====
    bookings = []  # List of upcoming bookings
    for b in fetch_upcoming_bookings():  # Get all upcoming bookings
        if not user_in_booking(b, current_user):  # Skip if current_user not in booking
            continue
        b_date = dt.datetime.strptime(b["date"], "%Y-%m-%d").date()  # Parse booking date
        b_end = dt.datetime.strptime(b["end"], "%I:%M %p").time()    # Parse booking end time
        # Booking is upcoming if: date > today OR (today but end time still in future)
        if b_date > today or (b_date == today and b_end > now.time()):
            bookings.append(b)

    # If no bookings found, show empty message
    if not bookings:
        ttk.Label(scroll_frame, text="You have no upcoming bookings.").pack(pady=20)
        return

    # Container frame for cards
    cards_frame = ttk.Frame(scroll_frame)
    cards_frame.pack(expand=True)

    max_per_row = 4  # Maximum cards per row
    for i, b in enumerate(bookings, start=1):  # Loop through upcoming bookings
        card = ttk.LabelFrame(cards_frame, text=f"My Booking #{i}", padding=10)  # Card for each booking
        row, col = divmod(i - 1, max_per_row)  # Compute row and column
        card.grid(row=row, column=col, padx=15, pady=15, sticky="n")  # Place card
        card.config(width=230)  # Set fixed width

        # Show booking details
        ttk.Label(card, text=f"📍 Venue: {b['venue']}").pack(anchor="w")
        ttk.Label(card, text=f"🏠 Room: {b['room']}").pack(anchor="w")
        ttk.Label(card, text=f"🗓 Date: {b['date']}").pack(anchor="w")
        ttk.Label(card, text=f"⏰ Time: {b['start']} – {b['end']}").pack(anchor="w")
        ttk.Label(card, text=f"👥 Pax: {b['pax']}").pack(anchor="w")
        ttk.Label(card, text=f"👤 Owner ID: {b['owner_id']}").pack(anchor="w")
        ttk.Label(card, text=f"👤 Owner Name: {b['owner_name']}").pack(anchor="w")

        # Show members if any
        members = b.get("members", "").strip()
        if members:
            ttk.Label(card, text="👥 Members:", font=("Arial", 10)).pack(anchor="w")
            for m in members.split(";"):        # Split member string by semicolon
                sid, sep, name = m.partition("|")  # Split into ID and Name
                ttk.Label(card, text=f"   • {sid} | {name}" if sep else f"   • {m}").pack(anchor="w", padx=15)

        # Cancel button only if current user is the booking owner
        if (b.get("owner_id", "").strip() == str(current_user).strip() or
            b.get("owner_name", "").strip().upper() == str(current_user).strip().upper()):
            def cancel_this_booking(b=b):  # Function to cancel booking
                if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel this booking?"):  # Confirmation
                    move_to_cancelled(b)  # Move to cancelled bookings
                    messagebox.showinfo("Cancelled", "Your booking has been cancelled.")  # Info popup
                    build_page(parent, current_user, back_callback)  # Refresh page

            tk.Button(  # Cancel button
                card, text="❌ Cancel", font=("Segoe UI", 9, "bold"),
                fg="white", bg="#e74c3c", activebackground="#c0392b",
                relief="flat", width=10,
                command=cancel_this_booking
            ).pack(anchor="e", pady=5)

    # Make columns expand evenly
    for col in range(max_per_row):
        cards_frame.grid_columnconfigure(col, weight=1)
