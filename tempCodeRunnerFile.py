import sqlite3

from flask import Flask, render_template, request, jsonify

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

@app.route('/api/increment_progress', methods=['POST'])
def increment_task():
    data = request.json
    task_id = data.get('id')

    if not task_id:
        return jsonify({"error": "No task selected"}), 400

    db = sqlite3.connect('productivity.db')
    cur = db.cursor()

    cur.execute("UPDATE tasks SET completed_pomodoros = completed_pomodoros + 1 WHERE id = ?", (task_id,))

    db.commit()
    db.close()

    # After db.close()
    return jsonify({"status": "success", "message": "Task progress updated!"})



    




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
    
def task_setup():
    db = sqlite3.connect('productivity.db')
    cur = db.cursor()

    cur.execute('''
            
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            total_pomodoros INTEGER DEFAULT 1,
            completed_pomodoros INTEGER DEFAULT 0
        )
        ''')
    db.commit()
    db.close()

task_setup()
    
@app.route('/api/add_item',methods=['POST'])
def add_tasks():
    # Grab the data from the frontend
    incoming_data = request.json
    item = incoming_data.get('name')

    # Connect the name to the task
    db = sqlite3.connect('productivity.db')
    cur = db.cursor()

    # Here we use INSERT INFO to ensure to save it and we just ? to protect from hacker using SQL Injection
    cur.execute("INSERT INTO tasks(title, total_pomodoros, completed_pomodoros) VALUES (?, ?, ?)", (item, 4, 0))

    db.commit()
    db.close()
    return "Item Saved."

@app.route('/api/get_task')
def show_tasks():
    db = sqlite3.connect('productivity.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM tasks")
    all_rows = cur.fetchall()

    db.close()
    return {f"Items": all_rows}

@app.route('/api/delete_task',methods=['DELETE'])
def delete_tasks():
    in_data = request.json
    target_task = in_data.get('id')

    connection = sqlite3.connect('productivity.db')


    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (target_task,))

    connection.commit()
    connection.close()
    print(f"DEBUG: Attempting to delete task with ID: {target_task}")

    return {"status": "success"}, 200



    

if __name__ == '__main__':
    app.run(debug=True)