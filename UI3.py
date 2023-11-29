import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the PIL Image to BytesIO
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")

    return img_bytes

# Function to display schedule for the selected day
def display_schedule(day, classes):
    st.write(f"Classes for {day}:")
    for class_name, class_time in classes.items():
        st.write(f"{class_name}: {class_time}")
        if st.button(f"Select {class_name}"):
            st.session_state.selected_class = class_name
            st.session_state.elevator_page = True

# Function to display elevator options and generate QR code
def display_elevator_page(selected_elevator):
    st.write(f"You selected {st.session_state.selected_class} on {st.session_state.selected_day}.")
    st.write(f"The floor you're going to is served by Elevator {selected_elevator}.")

    # QR code generation for the selected elevator
    qr_data = f"User: {st.session_state.user_id}\nClass: {st.session_state.selected_class}\nElevator: {selected_elevator}"
    qr_img = generate_qr_code(qr_data)
    st.image(qr_img, format="PNG", use_container_width=True)

# Main function to create the app
def main():
    st.title("ELEVATE App")

    # Home page
    if "user_id" not in st.session_state:
        st.write("Welcome to ELEVATE! This is the home page.")
        if st.button("Log In"):
            st.session_state.user_id = st.text_input("Enter your user ID")
            st.success(f"Logged in as {st.session_state.user_id}")

    # Schedule page
    elif "schedule" not in st.session_state:
        st.write(f"Welcome, {st.session_state.user_id}!")

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        selected_day = st.selectbox("Select a day", days_of_week)

        # Define classes for each day
        class_schedule = {
            "Monday": {"Technology": "12:00 PM", "Programming": "3:00 PM - 4:20 PM", "Algorithms": "4:30 PM - 5:50 PM"},
            "Tuesday": {"Class 1": "Time 1", "Class 2": "Time 2"},  # Add your classes here
            "Wednesday": {"Class 3": "Time 3", "Class 4": "Time 4"},  # Add your classes here
            "Thursday": {"Class 5": "Time 5", "Class 6": "Time 6"},    # Add your classes here
            "Friday": {"Class 7": "Time 7", "Class 8": "Time 8"},        # Add your classes here
        }

        st.session_state.selected_day = selected_day
        st.session_state.schedule = class_schedule[selected_day]
        display_schedule(selected_day, class_schedule[selected_day])

    # Elevator page
    elif "elevator_page" not in st.session_state:
        display_elevator_page(st.selectbox("Select an elevator", ["A", "B", "C"]))

        if st.button("Home"):
            st.session_state.pop("schedule")
            st.session_state.pop("selected_day")

if __name__ == "__main__":
    main()

