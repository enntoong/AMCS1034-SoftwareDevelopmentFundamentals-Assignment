# File: room_booking/main.py

import tkinter as tk                     # Import tkinter for GUI windows and widgets
from tkinter import ttk                  # Import ttk for themed widgets (modern look)

# Import other modules of the room booking system
from . import BookRoom                   # Booking page
from . import UpcomingBookings           # Upcoming bookings page
from . import CancelledBookings          # Cancelled bookings page
from . import PastBookings               # Past bookings page
from . import ViewAvailability           # Availability page
from .rooms_data import ROOMS            # Predefined rooms data dictionary


# Main window for the Discussion Room Booking system
class MainApp(tk.Toplevel):              # Inherit from Toplevel (new window)
    def __init__(self, parent, current_user):  # Initialize with parent window and current user
        super().__init__(parent)         # Call parent constructor
        self.parent = parent             # Save reference to parent
        self.current_user = current_user # Save current user info

        self.title("Discussion Room Booking")  # Window title
        self.geometry("1050x620")              # Window size
        self.configure(bg="#eef2f7")           # Background color

        self.rowconfigure(0, weight=1)         # Allow row 0 to expand
        self.columnconfigure(0, weight=1)      # Allow column 0 to expand

        self.content = ttk.Frame(self, padding=30)  # Main content frame
        self.content.grid(row=0, column=0, sticky="nsew")  # Place in grid, expand in all directions

        # ----- Custom style definitions -----
        style = ttk.Style()  # Create style object
        style.configure(
            "Card.TFrame",   # Custom style for card frames
            background="white",
            relief="raised"
        )
        style.configure(
            "Title.TLabel",  # Custom style for title labels
            font=("Segoe UI", 26, "bold"),
            foreground="#2c3e50"
        )
        style.configure(
            "TButton",       # Global button style
            font=("Segoe UI", 13, "bold"),
            padding=10
        )
        style.map(           # Button hover/active state style
            "TButton",
            background=[("active", "#3498db")],
            foreground=[("active", "white")]
        )

        self.show_dashboard()                       # Load dashboard view first
        self.protocol("WM_DELETE_WINDOW", self.back_to_home)  # Handle window close event

    def clear_content(self):  # Function to clear current content frame
        for widget in self.content.winfo_children():  # Loop all widgets
            widget.destroy()                          # Destroy them

    # ---------------- Dashboard ----------------
    def show_dashboard(self):   # Display dashboard page
        self.clear_content()    # Clear previous content

        dash = ttk.Frame(self.content, padding=40)  # Dashboard container
        dash.pack(expand=True)                      # Expand to center

        ttk.Label(  # Title label
            dash, text="📚 Discussion Room Booking",
            style="Title.TLabel"
        ).pack(pady=(0, 20))

        # White card container
        card = tk.Frame(
            dash, bg="white",                  # White background
            bd=0, relief="flat",               # No border, flat look
            highlightbackground="#dcdde1",     # Thin border color
            highlightthickness=1
        )
        card.pack(pady=20, ipadx=40, ipady=20)  # Add padding

        btn_frame = tk.Frame(card, bg="white")  # Frame for buttons
        btn_frame.pack(pady=10)

        # Helper function to create styled buttons
        def make_btn(text, cmd, color):
            btn = tk.Button(
                btn_frame,
                text=text,                     # Button text
                font=("Segoe UI", 12, "bold"), # Font style
                fg="white", bg=color,          # Text white, background custom color
                activebackground="#2c3e50",    # Background when active
                activeforeground="white",      # Text color when active
                relief="flat",                 # Flat button style
                width=20, height=2,            # Button size
                bd=0,                          # No border
                highlightthickness=0,          # No highlight border
                command=cmd                    # Function to call when clicked
            )
            btn.pack(side="left", padx=15, pady=10)  # Place side by side
            return btn

        # Dashboard main buttons
        make_btn("🏠 Book a Room", self.show_venues, "#3498db")               # Book a room button
        make_btn("📅 View Availability", self.show_availability_venues, "#27ae60")  # Availability button
        make_btn("🗂 My Bookings", lambda: self.show_page("mybookings"), "#f39c12") # My bookings menu button

        # Back button to return home
        tk.Button(
            dash, text="⬅ Back to Homepage",
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#7f8c8d",
            activebackground="#2c3e50",
            activeforeground="white",
            relief="flat",
            width=25, height=2,
            command=self.back_to_home
        ).pack(pady=30)

    # ---------------- Venue selection for booking ----------------
    def show_venues(self):  # Display venue selection for booking
        self.clear_content()  # Clear previous content
        ven = ttk.Frame(self.content, padding=30)  # Container frame
        ven.pack(expand=True)

        ttk.Label(  # Page title
            ven, text="🏟 Select a Venue",
            font=("Segoe UI", 20, "bold"),
            foreground="#2c3e50"
        ).pack(pady=20)

        btn_frame = ttk.Frame(ven)  # Frame for venue buttons
        btn_frame.pack(pady=20)

        # Custom color map for venues
        colors = {
            "Library": "#3498db",         # Blue
            "Cyber Center": "#27ae60",    # Green
            "Faculty Block A": "#f39c12", # Orange
            "Faculty Block B": "#8e44ad", # Purple
            "Student Hub": "#e74c3c",     # Red
            "Research Center": "#7f8c8d"  # Grey
        }

        col, row = 0, 0  # Grid counters
        for venue in ROOMS.keys():  # Loop through all venues
            color = colors.get(venue, "#34495e")  # Use custom color or default
            btn = tk.Button(
                btn_frame, text=venue,    # Venue name as button text
                width=20, height=2,
                font=("Segoe UI", 12, "bold"),
                fg="white", bg=color,
                activebackground="#2c3e50",
                activeforeground="white",
                relief="flat",
                command=lambda v=venue: self.show_page("book", v)  # Open booking page for this venue
            )
            btn.grid(row=row, column=col, padx=20, pady=15)  # Place in grid

            col += 1  # Move to next column
            if col > 1:  # Two buttons per row
                col = 0
                row += 1

        # Back button to dashboard
        tk.Button(
            ven, text="⬅ Back to Dashboard",
            width=20, height=2,
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#95a5a6",
            activebackground="#2c3e50",
            activeforeground="white",
            relief="flat",
            command=self.show_dashboard
        ).pack(pady=25)

    # ---------------- Venue selection for availability ----------------
    def show_availability_venues(self):  # Display venue selection for availability view
        self.clear_content()
        ven = ttk.Frame(self.content, padding=30)
        ven.pack(expand=True)

        ttk.Label(
            ven, text="📊 Select a Venue to View Availability",
            font=("Segoe UI", 20, "bold"),
            foreground="#2c3e50"
        ).pack(pady=20)

        btn_frame = ttk.Frame(ven)
        btn_frame.pack(pady=20)

        # Same custom color map as before
        colors = {
            "Library": "#3498db",
            "Cyber Center": "#27ae60",
            "Faculty Block A": "#f39c12",
            "Faculty Block B": "#8e44ad",
            "Student Hub": "#e74c3c",
            "Research Center": "#7f8c8d"
        }

        col, row = 0, 0
        for venue in ROOMS.keys():
            color = colors.get(venue, "#34495e")
            btn = tk.Button(
                btn_frame, text=venue,
                width=20, height=2,
                font=("Segoe UI", 12, "bold"),
                fg="white", bg=color,
                activebackground="#2c3e50",
                activeforeground="white",
                relief="flat",
                command=lambda v=venue: self.show_page("availability_table", v)  # Open availability page
            )
            btn.grid(row=row, column=col, padx=20, pady=15)

            col += 1
            if col > 1:
                col = 0
                row += 1

        # Back button to dashboard
        tk.Button(
            ven, text="⬅ Back to Dashboard",
            width=20, height=2,
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#95a5a6",
            activebackground="#2c3e50",
            activeforeground="white",
            relief="flat",
            command=self.show_dashboard
        ).pack(pady=25)

    # ---------------- Page dispatcher ----------------
    def show_page(self, name, venue=None):  # Function to load a page based on name
        self.clear_content()  # Clear current content
        page = ttk.Frame(self.content, padding=30)  # New frame for page
        page.pack(expand=True, fill="both")

        # Decide which page to show
        if name == "book":
            BookRoom.build_page(
                page,
                selected_venue=venue,
                current_user=self.current_user,
                back_callback=self.show_venues
            )
        elif name == "availability_table":
            ViewAvailability.build_page(
                page,
                selected_venue=venue,
                back_callback=self.show_availability_venues
            )
        elif name == "mybookings":
            self.show_my_bookings_menu(page)

    # ---------------- My Bookings menu ----------------
    def show_my_bookings_menu(self, parent):  # Display My Bookings menu
        for w in parent.winfo_children():  # Clear previous widgets
            w.destroy()

        ttk.Label(
            parent, text="🗂 My Bookings",
            font=("Segoe UI", 20, "bold"),
            foreground="#2c3e50"
        ).pack(pady=20)

        from . import UpcomingBookings, CancelledBookings, PastBookings  # Import here to avoid circular imports

        # Upcoming Bookings button (blue)
        tk.Button(
            parent, text="⏳ Upcoming Bookings",
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#3498db",
            activebackground="#2980b9",
            relief="flat", width=30, height=2,
            command=lambda: UpcomingBookings.build_page(
                parent, self.current_user,
                back_callback=lambda: self.show_my_bookings_menu(parent)
            )
        ).pack(pady=10)

        # Cancelled Bookings button (red)
        tk.Button(
            parent, text="❌ Cancelled Bookings",
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#e74c3c",
            activebackground="#c0392b",
            relief="flat", width=30, height=2,
            command=lambda: CancelledBookings.build_page(
                parent, self.current_user,
                back_callback=lambda: self.show_my_bookings_menu(parent)
            )
        ).pack(pady=10)

        # Past Bookings button (orange)
        tk.Button(
            parent, text="📜 Past Bookings",
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#f39c12",
            activebackground="#d35400",
            relief="flat", width=30, height=2,
            command=lambda: PastBookings.build_page(
                parent, self.current_user,
                back_callback=lambda: self.show_my_bookings_menu(parent)
            )
        ).pack(pady=10)

        # Back button to dashboard (grey)
        tk.Button(
            parent, text="⬅ Back to Dashboard",
            font=("Segoe UI", 12, "bold"),
            fg="white", bg="#95a5a6",
            activebackground="#7f8c8d",
            relief="flat", width=30, height=2,
            command=self.show_dashboard
        ).pack(pady=20)

    def back_to_home(self):  # Function to close this window and return to parent
        self.destroy()          # Destroy current window
        self.parent.deiconify() # Show parent window again
