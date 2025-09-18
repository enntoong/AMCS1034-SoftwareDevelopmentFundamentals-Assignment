# File: room_booking/helpers.py

def user_in_booking(b: dict, current_user: str) -> bool:  # Function to check if a user is in a booking
    """Check if the current user is part of the booking (Owner or Member)."""
    me = str(current_user).strip().upper()  # Normalize current_user (string, trimmed, uppercase)

    # --- Check Owner match ---
    if (  # Compare against booking owner info
        b.get("owner_name", "").strip().upper() == me   # Match by owner name (case-insensitive)
        or b.get("owner_id", "").strip() == str(current_user).strip()  # Match by owner ID
    ):
        return True  # User is the owner

    # --- Check Members match ---
    members = b.get("members", "").strip()  # Get members string from booking
    for m in members.split(";"):  # Split members by semicolon
        m = m.strip()  # Remove extra spaces
        if not m:  # Skip if empty string
            continue
        sid, sep, name = m.partition("|")  # Split member entry into ID and Name
        # Check if current_user matches either ID or Name
        if sid.strip() == str(current_user).strip() or name.strip().upper() == me:
            return True  # User is a member
    return False  # No match found
