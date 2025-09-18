# File: room_booking/BookRoom.py
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv
from .rooms_data import ROOMS

# Path to CSV files for storing bookings and user accounts
BOOKINGS_FILE = os.path.join("data", "bookings.csv")
USERS_FILE = os.path.join("data", "users.txt")


# ---------------- Student Data ----------------
def load_students():
    """Load student data {id: USERNAME} from users.txt"""
    if not os.path.exists(USERS_FILE):
        return {}
    students = {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:  # Format: student_id, username, password
                sid = parts[0].strip()
                username = parts[1].strip().upper()  # Store username in uppercase
                students[sid] = username
    return students


# Dictionary of students loaded at startup
STUDENTS = load_students()


# ---------------- Helpers ----------------
def get_next_5_days():
    """Return a list of the next 5 dates (YYYY-MM-DD) starting from today"""
    today = dt.date.today()
    return [(today + dt.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]


def generate_times(start_hour=8, end_hour=21, step=30):
    """Generate time slots between start_hour and end_hour with step (minutes)"""
    times, current = [], dt.datetime(2000, 1, 1, start_hour, 0)
    end = dt.datetime(2000, 1, 1, end_hour, 0)
    while current <= end:
        times.append(current.strftime("%I:%M %p").lstrip("0"))
        current += dt.timedelta(minutes=step)
    return times


# Precomputed available dates and times for booking
DATES, TIMES = get_next_5_days(), generate_times()


# ---------------- UI ----------------
def build_page(parent, selected_venue=None, current_user=None, back_callback=None):
    """Build the main booking page UI"""
    for w in parent.winfo_children():
        w.destroy()

    # Scrollable area for content
    canvas = tk.Canvas(parent, bg="#ecf0f1", highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    # Update scroll region when frame size changes
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frm = scroll_frame

    # Card container
    card = tk.Frame(frm, bg="white", bd=0, relief="flat")
    card.pack(fill="both", expand=True, pady=20, padx=20)

    # Title
    tk.Label(
        card,
        text="📝 Book a Discussion Room",
        font=("Segoe UI", 18, "bold"),
        fg="#2c3e50",
        bg="white"
    ).pack(pady=(20, 25))

    # Helper to add section labels
    def add_label(text):
        return tk.Label(card, text=text, font=("Segoe UI", 11, "bold"), fg="#2c3e50", bg="white", anchor="w")

    # Venue selection
    add_label("📍 Venue:").pack(fill="x", pady=(0, 5), padx=20)
    venue_var = tk.StringVar(value=selected_venue or "")
    venue_combo = ttk.Combobox(card, textvariable=venue_var, values=list(ROOMS.keys()), state="readonly")
    venue_combo.pack(fill="x", padx=20, pady=(0, 15))

    # Room selection
    add_label("🏠 Room:").pack(fill="x", pady=(0, 5), padx=20)
    room_var = tk.StringVar()
    room_combo = ttk.Combobox(card, textvariable=room_var, state="readonly")
    room_combo.pack(fill="x", padx=20, pady=(0, 5))
    info_label = tk.Label(card, text="Select a room to see details", fg="#7f8c8d", bg="white", anchor="w", justify="left")
    info_label.pack(fill="x", padx=20, pady=(0, 15))

    # Date selection
    add_label("🗓 Date:").pack(fill="x", pady=(0, 5), padx=20)
    date_var = tk.StringVar(value=DATES[0])
    ttk.Combobox(card, textvariable=date_var, values=DATES, state="readonly").pack(fill="x", padx=20, pady=(0, 15))

    # Start and End time selection
    add_label("⏰ Start:").pack(fill="x", pady=(0, 5), padx=20)
    start_var = tk.StringVar(value=TIMES[0])
    ttk.Combobox(card, textvariable=start_var, values=TIMES, state="readonly").pack(fill="x", padx=20, pady=(0, 15))

    add_label("⏰ End:").pack(fill="x", pady=(0, 5), padx=20)
    end_var = tk.StringVar(value=TIMES[1])
    ttk.Combobox(card, textvariable=end_var, values=TIMES, state="readonly").pack(fill="x", padx=20, pady=(0, 15))

    # Pax selection
    add_label("👥 Pax:").pack(fill="x", pady=(0, 5), padx=20)
    pax_var = tk.StringVar()
    pax_combo = ttk.Combobox(card, textvariable=pax_var, state="readonly")
    pax_combo.pack(fill="x", padx=20, pady=(0, 15))

    # Booking owner info
    owner_id, owner_name = None, None
    for sid, uname in STUDENTS.items():
        if uname.lower() == str(current_user).lower():
            owner_id, owner_name = sid, uname.upper()
            break
    if not owner_id:
        owner_id, owner_name = "N/A", str(current_user).upper()

    own_frame = tk.LabelFrame(card, text="👤 Booking Owner", font=("Segoe UI", 11, "bold"), bg="white", fg="#2c3e50", padx=15, pady=10)
    own_frame.pack(fill="x", padx=20, pady=(0, 15))
    tk.Label(own_frame, text=f"Student ID: {owner_id}", bg="white", anchor="w").pack(fill="x")
    tk.Label(own_frame, text=f"Name: {owner_name}", bg="white", anchor="w").pack(fill="x")

    # Other students section (auto-builds based on pax)
    mem_frame = tk.LabelFrame(card, text="👥 Other Students", font=("Segoe UI", 11, "bold"), bg="white", fg="#2c3e50", padx=15, pady=10)
    mem_frame.pack(fill="x", padx=20, pady=(0, 15))
    member_rows = []

    # Function to rebuild member rows whenever pax changes
    def rebuild_member_rows():
        nonlocal member_rows
        for child in mem_frame.winfo_children():
            child.destroy()
        member_rows = []
        if not pax_var.get().isdigit():
            return
        required = int(pax_var.get()) - 1
        if required <= 0:
            return
        tk.Label(mem_frame, text="Student ID      Name", bg="white", anchor="w").pack(fill="x")
        for _ in range(required):
            row = ttk.Frame(mem_frame)
            row.pack(fill="x", pady=2)
            id_ent = ttk.Entry(row, width=10)
            id_ent.pack(side="left", padx=3)
            name_ent = ttk.Entry(row)
            name_ent.pack(side="left", fill="x", expand=True, padx=3)

            # Auto uppercase names when focus leaves
            def to_uppercase(event, ent=name_ent):
                text = event.widget.get().strip().upper()
                ent.delete(0, tk.END)
                ent.insert(0, text)

            name_ent.bind("<FocusOut>", to_uppercase)
            member_rows.append((id_ent, name_ent))

    # Update functions when selecting venue/room/pax
    def update_rooms(_=None):
        venue = venue_var.get()
        if venue in ROOMS:
            room_combo["values"] = [r["name"] for r in ROOMS[venue]]
            room_combo.set("")
            info_label.config(text="Select a room to see details")
            pax_combo.set("")
            pax_combo["values"] = []
            rebuild_member_rows()

    def update_room_info(_=None):
        venue, room_name = venue_var.get(), room_var.get()
        if not (venue and room_name):
            return
        for r in ROOMS[venue]:
            if r["name"] == room_name:
                cap_list, eq = r["capacity"], ", ".join(r["equipment"])

                # Format capacity display
                if not cap_list:
                    cap_range = "N/A"
                elif len(cap_list) == 1:
                    cap_range = str(cap_list[0])
                else:
                    cap_range = f"{min(cap_list)} – {max(cap_list)}"

                info_label.config(
                    text=f"Capacity: {cap_range}\nEquipment: {eq}",
                    fg="#2c3e50", justify="left", anchor="w"
                )
                pax_combo["values"] = [str(x) for x in cap_list]
                pax_combo.set("")
                rebuild_member_rows()
                break

    # Bind combobox events
    venue_combo.bind("<<ComboboxSelected>>", update_rooms)
    room_combo.bind("<<ComboboxSelected>>", update_room_info)
    pax_combo.bind("<<ComboboxSelected>>", lambda e: rebuild_member_rows())

    if selected_venue and selected_venue in ROOMS:
        update_rooms()

    # Buttons (Back / Confirm Booking)
    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(pady=20)

    back_btn = tk.Button(
        btn_frame, text="⬅ Back",
        font=("Segoe UI", 11, "bold"),
        bg="#95a5a6", fg="white", activebackground="#7f8c8d",
        padx=20, pady=8, bd=0, relief="flat", cursor="hand2",
        command=lambda: back_callback() if back_callback else None
    )
    back_btn.pack(side="left", padx=10)

    confirm_btn = tk.Button(
        btn_frame, text="✅ Confirm Booking",
        font=("Segoe UI", 11, "bold"),
        bg="#27ae60", fg="white", activebackground="#219150",
        padx=25, pady=8, bd=0, relief="flat", cursor="hand2",
        command=lambda: confirm_booking(
            venue_var, room_var, date_var, start_var, end_var,
            pax_var, owner_id, owner_name, member_rows
        )
    )
    confirm_btn.pack(side="left", padx=10)


# ---------------- Validation & Save ----------------
def confirm_booking(venue_var, room_var, date_var, start_var, end_var,
                    pax_var, owner_id, owner_name, member_rows):
    """Validate booking form, check conflicts, then save booking if valid"""
    # --- Basic checks ---
    if not venue_var.get():
        messagebox.showerror("Error", "Please select a venue.")
        return
    if not room_var.get():
        messagebox.showerror("Error", "Please select a room.")
        return
    if not pax_var.get().isdigit():
        messagebox.showerror("Error", "Please choose pax.")
        return

    # Duration validation
    start_idx, end_idx = TIMES.index(start_var.get()), TIMES.index(end_var.get())
    duration_minutes = (end_idx - start_idx) * 30
    if duration_minutes <= 0:
        messagebox.showerror("Error", "End time must be after start time.")
        return
    if duration_minutes > 180:
        messagebox.showerror("Error", "Booking cannot exceed 3 hours.")
        return

    # Date validation
    chosen_date = dt.datetime.strptime(date_var.get(), "%Y-%m-%d").date()
    today = dt.date.today()
    if chosen_date < today:
        messagebox.showerror("Error", "Date cannot be in the past.")
        return

    # Time validation if booking for today
    if chosen_date == today:
        now = dt.datetime.now().time()
        start_time = dt.datetime.strptime(start_var.get(), "%I:%M %p").time()
        if start_time <= now:
            messagebox.showerror("Error", "You cannot book a time that has already passed today.")
            return

    # --- Availability check ---
    for b in fetch_bookings():
        if b["date"] == date_var.get():
            b_start = dt.datetime.strptime(b["start"], "%I:%M %p").time()
            b_end = dt.datetime.strptime(b["end"], "%I:%M %p").time()

            new_start = dt.datetime.strptime(start_var.get(), "%I:%M %p").time()
            new_end = dt.datetime.strptime(end_var.get(), "%I:%M %p").time()

            # Check for overlap
            if not (new_end <= b_start or new_start >= b_end):
                # Owner double booking
                if b["owner_id"] == owner_id:
                    messagebox.showerror(
                        "Error",
                        f"You already have a booking in this time slot!\n\n"
                    )
                    return
                # Room occupied by another booking
                if b["venue"] == venue_var.get() and b["room"] == room_var.get():
                    messagebox.showerror(
                        "Error",
                        f"This time slot is already booked for the selected room!\n\n"
                    )
                    return

    # --- Members validation ---
    required = int(pax_var.get()) - 1
    members = []
    seen_ids = set()

    for i, (id_ent, name_ent) in enumerate(member_rows, start=1):
        sid, sname = id_ent.get().strip(), name_ent.get().strip().upper()
        if not sid or not sname:
            messagebox.showerror("Error", f"Please complete member row #{i} (ID & Name).")
            return
        if sid == owner_id:
            messagebox.showerror("Error", f"Row {i}: Owner cannot be added again.")
            return
        expected_name = STUDENTS.get(sid)
        if expected_name is None or expected_name != sname:
            messagebox.showerror("Error", f"Row {i}: Invalid student info ({sid} / {sname}).")
            return
        if sid in seen_ids:
            messagebox.showerror("Error", f"Row {i}: Duplicate student ID {sid}.")
            return
        seen_ids.add(sid)
        members.append({"id": sid, "name": expected_name})

    if len(members) != required:
        messagebox.showerror("Error", "Please fill exactly the required number of members.")
        return

    # --- Save booking ---
    booking = {
        "venue": venue_var.get(),
        "room": room_var.get(),
        "date": date_var.get(),
        "start": start_var.get(),
        "end": end_var.get(),
        "pax": pax_var.get(),
        "owner_id": owner_id,
        "owner_name": owner_name.upper(),
        "members": "; ".join([f"{m['id']}|{m['name']}" for m in members])
    }
    save_booking(booking)

    messagebox.showinfo(
        "Success",
        f"Booked!\n"
        f"📍Venue : {booking['venue']}\n"
        f"🏠Room : {booking['room']}\n"
        f"🗓Date : {booking['date']}\n"
        f"⏰Time : {booking['start']} - {booking['end']}\n"
        f"👥Pax : {booking['pax']}"
    )


# ---------------- CSV ----------------
def init_db():
    """Initialize bookings.csv with headers if not exists"""
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "venue", "room", "date", "start", "end", "pax",
                "owner_id", "owner_name", "members"
            ]
            csv.DictWriter(f, fieldnames=fieldnames).writeheader()


def save_booking(data: dict):
    """Append a booking record to bookings.csv"""
    init_db()
    with open(BOOKINGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "venue", "room", "date", "start", "end", "pax",
            "owner_id", "owner_name", "members"
        ])
        writer.writerow(data)


def fetch_bookings():
    """Fetch all bookings as a list of dictionaries"""
    if not os.path.exists(BOOKINGS_FILE):
        return []
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fetch_upcoming_bookings():
    """Return only bookings from today onwards"""
    all_bookings = fetch_bookings()
    today = dt.date.today()
    upcoming = []
    for b in all_bookings:
        try:
            b_date = dt.datetime.strptime(b["date"], "%Y-%m-%d").date()
            if b_date >= today:
                upcoming.append(b)
        except Exception:
            continue
    return upcoming
