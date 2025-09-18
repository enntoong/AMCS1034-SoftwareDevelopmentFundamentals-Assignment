# File: room_booking/ViewAvailability.py

import tkinter as tk                  # Import tkinter for GUI
from tkinter import ttk               # Import ttk for modern themed widgets
import datetime as dt                 # Import datetime for date/time handling
import csv                            # Import csv for reading/writing booking files
import os                             # Import os for file path handling
from .rooms_data import ROOMS         # Import predefined rooms data dictionary

BOOKINGS_FILE = os.path.join("data", "bookings.csv")  # Path to active bookings file


# ---------------- Helpers ----------------
def get_next_5_days():  # Generate a list of today + next 4 days
    today = dt.date.today()
    return [(today + dt.timedelta(days=i)) for i in range(5)]


def generate_times(start_hour=8, end_hour=21, step=30):  # Generate time slots (HH:MM)
    times, current = [], dt.datetime(2000, 1, 1, start_hour, 0)  # Start at given hour
    end = dt.datetime(2000, 1, 1, end_hour, 0)                   # End at given hour
    while current <= end:  # Keep looping until end time
        times.append(current.strftime("%I:%M %p").lstrip("0"))   # Format time like 9:00 AM
        current += dt.timedelta(minutes=step)                    # Step forward
    return times


DATES = get_next_5_days()  # Preload next 5 days
TIMES = generate_times()   # Preload time slots from 8:00–21:00


def fetch_bookings():  # Load all bookings from file
    if not os.path.exists(BOOKINGS_FILE):
        return []
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))  # Return list of booking dictionaries


# ---------------- Show Room Detail ----------------
def show_room_detail(room):  # Pop-up window with detailed info about a room
    detail_win = tk.Toplevel()                      # New top-level window
    detail_win.title(f"Room Detail – {room['name']}")  # Window title
    detail_win.geometry("400x350")                  # Window size

    # === Scrollable Frame ===
    container = ttk.Frame(detail_win)               # Outer container
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, highlightthickness=0)   # Canvas for scroll
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)  # Vertical scroll
    scroll_frame = ttk.Frame(canvas)                # Inner frame

    scroll_frame.bind(  # Update scroll region on resize
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")  # Add frame inside canvas
    canvas.configure(yscrollcommand=scrollbar.set)                  # Connect scrollbar

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === Content ===
    ttk.Label(scroll_frame, text=f"🏠 {room['name']}",
              font=("Segoe UI", 16, "bold")).pack(pady=10)

    # Room detail fields
    fields = {
        "Venue Type": room.get("venue_type", ""),
        "Venue No.": room.get("name", ""),
        "Location": room.get("location", ""),
        "Min/Max Pax": f"{min(room['capacity'])} – {max(room['capacity'])}",
        "Equipment": ", ".join(room.get("equipment", [])),
        "Description": room.get("description", "")
    }

    # Display each field as row
    for key, val in fields.items():
        row = ttk.Frame(scroll_frame)
        row.pack(fill="x", pady=4, padx=15)
        ttk.Label(row, text=f"{key}:", width=15, anchor="w",
                  font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Label(row, text=val, anchor="w").pack(side="left", fill="x", expand=True)

    # === Close button ===
    ttk.Button(
        scroll_frame,
        text="❌ Close",
        width=12,
        command=detail_win.destroy
    ).pack(pady=15)


# ---------------- UI ----------------
def build_page(parent, selected_venue=None, back_callback=None):  # Build availability page
    for w in parent.winfo_children():  # Clear parent frame
        w.destroy()

    # White background full page container
    card = tk.Frame(parent, bg="white", bd=0, relief="flat")
    card.pack(fill="both", expand=True)

    # ---------------- Title ----------------
    ttk.Label(
        card, text=f"📅 Availability – {selected_venue}",
        font=("Segoe UI", 18, "bold"),
        background="white"
    ).pack(pady=10)

    bookings = fetch_bookings()               # Load all bookings
    rooms = ROOMS.get(selected_venue, [])     # Get rooms for this venue

    # ---------------- Date Selector ----------------
    date_var = tk.StringVar(value=DATES[0].strftime("%Y-%m-%d"))  # Default date
    date_options = [d.strftime("%Y-%m-%d") for d in DATES]        # List of options

    top_frame = ttk.Frame(card)   # Frame for date selector
    top_frame.pack(pady=5)
    ttk.Label(top_frame, text="Select Date:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
    ttk.Combobox(top_frame, textvariable=date_var, values=date_options,
                 state="readonly", width=12).pack(side="left")

    # ---------------- Legend ----------------
    legend = tk.Frame(card, bg="white")
    legend.pack(pady=5)

    # Helper to add colored legend box + label
    def add_legend(color, text):
        c = tk.Canvas(legend, width=20, height=20, highlightthickness=1)
        c.create_rectangle(0, 0, 20, 20, fill=color, outline="black")
        c.pack(side="left", padx=3)
        tk.Label(legend, text=text, font=("Segoe UI", 10), bg="white").pack(side="left", padx=10)

    add_legend("green", "Available")
    add_legend("blue", "Booked")
    add_legend("gray", "Unavailable (Past)")

    # ---------------- Back button ----------------
    tk.Button(
        card, text="⬅ Back",
        font=("Segoe UI", 11, "bold"),
        bg="#95a5a6", fg="white", activebackground="#7f8c8d",
        width=18, height=1,
        relief="flat", cursor="hand2",
        command=lambda: back_callback() if back_callback else None
    ).pack(pady=10)

    # ---------------- Scrollable Canvas ----------------
    canvas = tk.Canvas(card, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------------- Draw Grid ----------------
    def draw_grid():  # Function to draw availability table
        for w in scroll_frame.winfo_children():  # Clear old grid
            w.destroy()

        chosen_date = date_var.get()                         # Selected date
        today_str = dt.date.today().strftime("%Y-%m-%d")     # Today's date string
        now_time = dt.datetime.now().time()                  # Current time

        # Header row
        tk.Label(scroll_frame, text="Time", font=("Segoe UI", 10, "bold"), width=16).grid(row=0, column=0, padx=1, pady=1)
        for j, r in enumerate(rooms, start=1):
            tk.Button(
                scroll_frame,
                text=r["name"],             # Room name
                font=("Segoe UI", 10, "bold"),
                width=20,
                wraplength=120,             # Wrap text if too long
                bg="#f0f0f0",               # Light grey background
                command=lambda room=r: show_room_detail(room)  # Click → show detail popup
            ).grid(row=0, column=j, padx=1, pady=1)

        # Time slots grid
        for i in range(len(TIMES) - 1):
            start = TIMES[i]
            end = TIMES[i + 1]
            label = f"{start} - {end}"  # Example: 9:00 AM – 9:30 AM

            tk.Label(scroll_frame, text=label, width=16, anchor="w").grid(row=i+1, column=0, padx=1, pady=1)

            start_time = dt.datetime.strptime(start, "%I:%M %p").time()
            end_time = dt.datetime.strptime(end, "%I:%M %p").time()

            for j, r in enumerate(rooms, start=1):
                color = "green"  # Default: available

                # 1. Check if booked (overlap with booking interval)
                for b in bookings:
                    if (
                        b["venue"] == selected_venue
                        and b["room"] == r["name"]
                        and b["date"] == chosen_date
                    ):
                        b_start = dt.datetime.strptime(b["start"], "%I:%M %p").time()
                        b_end = dt.datetime.strptime(b["end"], "%I:%M %p").time()

                        # Overlap check
                        if not (end_time <= b_start or start_time >= b_end):
                            color = "blue"  # Booked
                            break

                # 2. Past time check (only if today, not booked yet)
                if color == "green" and chosen_date == today_str and end_time <= now_time:
                    color = "gray"  # Past

                # Draw block
                block = tk.Canvas(scroll_frame, width=100, height=20, highlightthickness=0)
                block.grid(row=i+1, column=j, padx=1, pady=1)
                block.create_rectangle(0, 0, 100, 20, fill=color, outline="black")

    # Re-draw grid whenever date changes
    date_var.trace_add("write", lambda *_: draw_grid())
    draw_grid()  # Initial draw
