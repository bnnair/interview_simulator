from flask import Flask, render_template
import sqlite3
from pathlib import Path
import os

app = Flask(__name__)

def clean_text(text):
    # Remove quotes and special characters
    text = text.strip().replace('"', '').replace("'", '')
    text = text.replace("\\n\\n", "<br/>").replace("\\n","<br/>").strip()
    text = text.replace("\\","").strip()
    # Replace multiple newlines with single space
    # text = ' '.join(text.split('\n'))
    return text

@app.route('/')
def display_data():
    "interview-simulator/backend/app/interview.db"
    db_parent = Path(__file__).resolve().parent.parent
    print(f"db parent folder ----> {db_parent}")
    db_path = os.path.join(db_parent,"backend","app","interview.db")
    print(f"dp path -------->: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Replace 'your_table' and 'text_column' with actual names
    cursor.execute("SELECT id, resume_id, question, answer FROM interview_sessions")
    rows = cursor.fetchall()
    
    data_list= []
    clean_data = {}
    for row in rows:
        print(f"row -----: {row}")
        id = row[0]
        question = clean_text(row[2])
        print(f"question -----> {question}")
        answer = clean_text(row[3])    
        print(f"answer -----> {answer}")
        clean_data = {"id": id, "question": question , "answer" : answer}
        
        data_list.append(clean_data)
    
    conn.close()
    return render_template('display.html', contents=data_list)

if __name__ == '__main__':
    app.run(debug=True)
