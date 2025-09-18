# File: room_booking/PastBookings.py

import tkinter as tk                        # Import tkinter for GUI components
from tkinter import ttk                     # Import ttk for themed widgets
import os, csv, datetime as dt              # Import os (file handling), csv (read/write), datetime (time operations)
from .helpers import user_in_booking        # Import helper function to check if user is in a booking

# File path for all bookings (not only past)
BOOKINGS_FILE = os.path.join("data", "bookings.csv")

def fetch_past_bookings():  # Function to load all bookings from CSV file
    if not os.path.exists(BOOKINGS_FILE):   # If file not found, return empty list
        return []
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:  # Open bookings file
        return list(csv.DictReader(f))  # Return list of booking dictionaries

def build_page(parent, current_user, back_callback=None):  # Function to build "Past Bookings" page
    for w in parent.winfo_children():      # Remove all widgets in parent frame
        w.destroy()

    now = dt.datetime.now()                # Get current date and time
    today = now.date()                     # Extract today's date

    # ===== Header =====
    title_frame = ttk.Frame(parent)        # Header container
    title_frame.pack(fill="x", pady=10)    # Place at top with padding

    # Page title label
    ttk.Label(
        title_frame, text="📖 My Past Bookings",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=10)

    # Back button (calls back_callback if given)
    ttk.Button(
        title_frame, text="⬅ Back", width=10,
        command=(lambda: back_callback()) if back_callback else None
    ).pack(side="right", padx=5)

    # ===== Scrollable =====
    canvas = tk.Canvas(parent)                       # Create canvas for scrolling content
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)  # Vertical scrollbar
    scroll_frame = ttk.Frame(canvas, padding=10)     # Inner frame inside canvas
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  # Update scroll region
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")  # Place scroll_frame inside canvas
    canvas.configure(yscrollcommand=scrollbar.set)   # Link canvas scroll to scrollbar
    canvas.pack(side="left", fill="both", expand=True)  # Pack canvas left side
    scrollbar.pack(side="right", fill="y")           # Pack scrollbar right side

    # ===== Data =====
    bookings = []                                    # List to store valid past bookings
    for b in fetch_past_bookings():                  # Loop through all bookings
        if not user_in_booking(b, current_user):     # Skip if current_user not in booking
            continue
        b_date = dt.datetime.strptime(b["date"], "%Y-%m-%d").date()  # Parse booking date
        b_end = dt.datetime.strptime(b["end"], "%I:%M %p").time()    # Parse booking end time
        # Booking is in the past if: date < today OR (same date but already ended)
        if b_date < today or (b_date == today and b_end <= now.time()):
            bookings.append(b)

    # If no past bookings, show empty message
    if not bookings:
        ttk.Label(scroll_frame, text="You have no past bookings.").pack(pady=20)
        return

    # Frame to hold booking cards
    cards_frame = ttk.Frame(scroll_frame)
    cards_frame.pack(expand=True)

    max_per_row = 4  # Number of cards per row
    for i, b in enumerate(bookings, start=1):  # Loop through bookings
        card = ttk.LabelFrame(cards_frame, text=f"Past Booking #{i}", padding=10)  # Card frame
        row, col = divmod(i - 1, max_per_row)  # Compute row and column in grid
        card.grid(row=row, column=col, padx=15, pady=15, sticky="n")  # Place in grid
        card.config(width=230)  # Set fixed width for card

        # Show booking details
        ttk.Label(card, text=f"📍 Venue: {b['venue']}").pack(anchor="w")
        ttk.Label(card, text=f"🏠 Room: {b['room']}").pack(anchor="w")
        ttk.Label(card, text=f"🗓 Date: {b['date']}").pack(anchor="w")
        ttk.Label(card, text=f"⏰ Time: {b['start']} – {b['end']}").pack(anchor="w")
        ttk.Label(card, text=f"👥 Pax: {b['pax']}").pack(anchor="w")
        ttk.Label(card, text=f"👤 Owner ID: {b['owner_id']}").pack(anchor="w")
        ttk.Label(card, text=f"👤 Owner Name: {b['owner_name']}").pack(anchor="w")

        # Show members if available
        members = b.get("members", "").strip()  # Get member string
        if members:
            ttk.Label(card, text="👥 Members:", font=("Arial", 10)).pack(anchor="w")
            for m in members.split(";"):        # Split by semicolon
                sid, sep, name = m.partition("|")  # Split each member into ID and name
                # Display formatted line (ID | Name) if both exist
                ttk.Label(card, text=f"   • {sid} | {name}" if sep else f"   • {m}").pack(anchor="w", padx=15)

    # Make grid columns expand equally
    for col in range(max_per_row):
        cards_frame.grid_columnconfigure(col, weight=1)
