# File: room_booking/CancelledBookings.py

import tkinter as tk                      # Import tkinter for GUI components
from tkinter import ttk                   # Import ttk for themed (modern) widgets
import os, csv                            # Import os for file paths, csv for reading/writing CSV files
from .helpers import user_in_booking      # Import helper function to check if user is involved in a booking

# File path for storing cancelled bookings
CANCELLED_FILE = os.path.join("data", "cancelled_bookings.csv")

def fetch_cancelled_bookings():  # Function to load cancelled bookings from CSV
    if not os.path.exists(CANCELLED_FILE):  # If file does not exist, return empty list
        return []
    with open(CANCELLED_FILE, "r", encoding="utf-8") as f:  # Open cancelled bookings file
        return list(csv.DictReader(f))  # Read rows into list of dictionaries

def build_page(parent, current_user, back_callback=None):  # Function to build cancelled bookings page
    for w in parent.winfo_children():  # Clear all existing widgets from parent
        w.destroy()

    # ===== Header =====
    title_frame = ttk.Frame(parent)  # Create frame for header
    title_frame.pack(fill="x", pady=10)  # Pack header frame across x-axis with padding

    # Header title label
    ttk.Label(
        title_frame,
        text="❌ My Cancelled Bookings",  # Title text
        font=("Arial", 18, "bold")       # Font style
    ).pack(side="left", padx=10)         # Place on left with padding

    # Back button to return to previous page
    ttk.Button(
        title_frame,
        text="⬅ Back",                   # Button text
        width=10,                        # Button width
        command=(lambda: back_callback()) if back_callback else None  # Call back_callback if provided
    ).pack(side="right", padx=5)         # Place button on right with padding

    # ===== Scrollable =====
    canvas = tk.Canvas(parent)  # Create canvas for scrollable content
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)  # Vertical scrollbar
    scroll_frame = ttk.Frame(canvas, padding=10)  # Inner frame inside canvas with padding

    # Update scroll region when inner frame changes size
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")  # Place frame inside canvas
    canvas.configure(yscrollcommand=scrollbar.set)  # Connect scrollbar to canvas

    canvas.pack(side="left", fill="both", expand=True)  # Pack canvas on left, expand to fill
    scrollbar.pack(side="right", fill="y")  # Pack scrollbar on right

    # ===== Data =====
    # Filter cancelled bookings to only include ones involving current_user
    bookings = [b for b in fetch_cancelled_bookings() if user_in_booking(b, current_user)]

    # If user has no cancelled bookings, show message and return
    if not bookings:
        ttk.Label(scroll_frame, text="You have no cancelled bookings.").pack(pady=20)
        return

    # Container frame for booking cards
    cards_frame = ttk.Frame(scroll_frame)
    cards_frame.pack(expand=True)

    max_per_row = 4  # Maximum number of cards per row

    # Loop through bookings and display each as a card
    for i, b in enumerate(bookings, start=1):
        card = ttk.LabelFrame(cards_frame, text=f"Cancelled Booking #{i}", padding=10)  # Card frame
        row, col = divmod(i - 1, max_per_row)  # Calculate row and column position
        card.grid(row=row, column=col, padx=15, pady=15, sticky="n")  # Place card in grid
        card.config(width=230)  # Set card width

        # Show booking details inside card
        ttk.Label(card, text=f"📍 Venue: {b['venue']}").pack(anchor="w")
        ttk.Label(card, text=f"🏠 Room: {b['room']}").pack(anchor="w")
        ttk.Label(card, text=f"🗓 Date: {b['date']}").pack(anchor="w")
        ttk.Label(card, text=f"⏰ Time: {b['start']} – {b['end']}").pack(anchor="w")
        ttk.Label(card, text=f"👥 Pax: {b['pax']}").pack(anchor="w")
        ttk.Label(card, text=f"👤 Owner ID: {b['owner_id']}").pack(anchor="w")
        ttk.Label(card, text=f"👤 Owner Name: {b['owner_name']}").pack(anchor="w")

        # Show member list if available
        members = b.get("members", "").strip()  # Get members string
        if members:
            ttk.Label(card, text="👥 Members:", font=("Arial", 10)).pack(anchor="w")  # Section title
            for m in members.split(";"):  # Split members by semicolon
                sid, sep, name = m.partition("|")  # Split into student ID and name
                # Display properly formatted member line
                ttk.Label(card, text=f"   • {sid} | {name}" if sep else f"   • {m}").pack(anchor="w", padx=15)

    # Ensure all grid columns expand equally
    for col in range(max_per_row):
        cards_frame.grid_columnconfigure(col, weight=1)
