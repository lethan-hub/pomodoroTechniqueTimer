import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

# This is the single source of truth for your app
pomodoro_count = 0
session_playlist = ["Work", "Short Break", "Work", "Short Break", "Work", "Short Break", "Work", "Long Break"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/next')
def next_round():
    global pomodoro_count
    pomodoro_count += 1
    print(f"Counter advanced to: {pomodoro_count}")
    return "Success"

@app.route('/api/timer/status')
def get_timer_status():
    global pomodoro_count
    
    # Use the modulo math to find where we are in the playlist
    current_phase = session_playlist[pomodoro_count % len(session_playlist)]
    
    # Send the correct data back to JavaScript
    if current_phase == "Work":
        # Using 1500 for real work, or change to 10 for testing
        return {"seconds": 1500, "phase": "Work"}
    elif current_phase == "Short Break":
        # This handles both Short and Long breaks from your list
        return {"seconds": 300, "phase": "Short Break"}
    else:
        return {"seconds": 900, "phase": "Long Break"}

@app.route('/jump/<phase_name>')
def jump_to_phase(phase_name):
    global pomodoro_count

    try:
        pomodoro_count = session_playlist.index(phase_name)
        print(f"Manual Jump! Counter is now {pomodoro_count}")
        return "Jump Successful"
    except ValueError:
        # This part handles it if you send a name that isn't in the list
        return "Phase not found", 404
    
@app.route('/api/add_item',methods=['POST'])
def add_tasks():
    # Grab the data from the frontend
    incoming_data = request.json
    item = incoming_data.get('name')

    # Connect the name to the task
    db = sqlite3.connect('productivity.db')
    cur = db.cursor()

    # Here we use INSERT INFO to ensure to save it and we just ? to protect from hacker using SQL Injection
    cur.execute("INSERT INFO tasks(title) VALUES (?)",(item, "Unknown"))

    db.commit()
    db.close()
    return "Item Saved."





    

if __name__ == '__main__':
    app.run(debug=True)