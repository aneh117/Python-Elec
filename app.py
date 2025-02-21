from flask import Flask, render_template, request
import sqlite3
import requests

# Telegram bot details
TOKEN2 = "7547168681:AAFOMetVjyTejjOEjKfVMRBv0EJ68nJ6Sb0"
chat_id2 = "6267940035"
message_template = "Fire detected at {address}"  
# URL for Telegram API
def send_telegram_message(message):
    url1 = f"https://api.telegram.org/bot{TOKEN2}/sendMessage?chat_id={chat_id2}&text={message}"
    response = requests.get(url1)
    return response.json()

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('fire_alarm.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        address TEXT)''')
    conn.commit()
    conn.close()

# Fetch the latest address and send a Telegram message at the start
def send_fire_alert():
    conn = sqlite3.connect('fire_alarm.db')
    cursor = conn.cursor()

    # Fetch the latest address
    cursor.execute("SELECT address FROM users WHERE id = 1")
    latest_address = cursor.fetchone()

    # If address is found, format and send the message
    if latest_address:
        address = latest_address[0]
        message = message_template.format(address=address)
        send_telegram_message(message)
        print(f"Telegram message sent: {message}")
    else:
        print("No address found in the database.")

    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    # ThingSpeak chart URLs
    thingspeak_url_1 = "https://thingspeak.com/channels/2819075/charts/1/?api_key=TOFXYGJHDUUENR03"
    thingspeak_url_2 = "https://thingspeak.com/channels/2819075/charts/2/?api_key=TOFXYGJHDUUENR03"

    return render_template("index.html", 
                           graph_url_1=thingspeak_url_1, 
                           graph_url_2=thingspeak_url_2)

@app.route("/address", methods=["GET", "POST"])
def address():
    conn = sqlite3.connect("fire_alarm.db")
    cursor = conn.cursor()

    if request.method == "POST":
        user_address = request.form["address"]

        # Log the address received from the form
        print(f"Address received: {user_address}")

        # Use REPLACE INTO to ensure only one row exists (this will overwrite the old address)
        cursor.execute("REPLACE INTO users (id, address) VALUES (1, ?)", (user_address,))
        conn.commit()
        print("Address saved to database.")

    # Fetch the latest address
    cursor.execute("SELECT address FROM users WHERE id = 1")
    latest_address = cursor.fetchone()

    print(f"Fetched address: {latest_address}")

    conn.close()

    return render_template("address.html", address=latest_address[0] if latest_address else None)

def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)
    
if __name__ == "__main__":
    init_db()  # Initialize the database when the app starts
    send_fire_alert()  # Send the fire alert when the app starts with the latest address
    run_flask()






