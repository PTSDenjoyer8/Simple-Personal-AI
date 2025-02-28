import os
import time
import random
import sqlite3
import ollama
import pyautogui
import psutil
import subprocess
import glob

AI_NAME = "Athena"

conn = sqlite3.connect("athena_memory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    ai_response TEXT
)
""")
conn.commit()

def save_to_memory(user_input, ai_response):
    cursor.execute("INSERT INTO memory (user_input, ai_response) VALUES (?, ?)", (user_input, ai_response))
    conn.commit()

def get_last_conversations(limit=5):
    cursor.execute("SELECT user_input, ai_response FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    return cursor.fetchall()

def ask_ollama(question):
    history = get_last_conversations()
    history_text = "\n".join([f"User: {h[0]}\nAthena: {h[1]}" for h in history])
    
    system_prompt = f"You are an AI assistant named {AI_NAME}. Always introduce yourself as {AI_NAME}.\n\nRecent conversation history:\n{history_text}"

    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ])
    
    return response['message']['content']

def initiate_conversation():
    prompts = [
        f"I am {AI_NAME}, how can I assist you today?",
        f"Hey! I'm {AI_NAME}. Do you need anything?",
        f"Hello! I am {AI_NAME}, would you like to discuss something?"
    ]
    return random.choice(prompts)

def open_application(app_name):
    try:
        command = f'powershell -command "&{{(Get-StartApps | Where-Object {{$_.Name -match \"{app_name}\"}}).AppID}}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        found_apps = result.stdout.strip().split("\n")

        found_apps = [app.strip() for app in found_apps if app.strip()]
        if len(found_apps) > 1:
            print(f"Multiple applications found: {', '.join(found_apps)}")
            selected_app = input("Please type the full name of the application you want to open: ").strip()
            
            if selected_app in found_apps:
                subprocess.Popen(f"explorer shell:AppsFolder\\{selected_app}", shell=True)
                return f"Opened {selected_app}"
            else:
                return "Invalid selection. Please try again."

        if len(found_apps) == 1:
            subprocess.Popen(f"explorer shell:AppsFolder\\{found_apps[0]}", shell=True)
            return f"Opened {found_apps[0]}"

        possible_paths = [
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs")
        ]

        for path in possible_paths:
            if os.path.exists(path):
                for file in glob.glob(path + "\\**\\*.lnk", recursive=True):
                    if app_name.lower() in os.path.basename(file).lower():
                        subprocess.Popen(file, shell=True)
                        return f"Opened {app_name} from Start Menu shortcuts"

        return f"Application {app_name} not found"

    except Exception as e:
        return f"Error opening {app_name}: {e}"

def close_application(app_name):
    try:
        found = False
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                psutil.Process(process.info['pid']).terminate()
                found = True
                print(f"Closed {process.info['name']} (PID: {process.info['pid']})")
        
        if found:
            return f"Closed {app_name} successfully"
        
        result = subprocess.run(["taskkill", "/F", "/IM", f"{app_name}.exe"], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            return f"Force closed {app_name}"
        
        return f"No process found matching {app_name}"
    
    except Exception as e:
        return f"Error closing {app_name}: {e}"

def process_command(user_input):
    try:
        words = user_input.lower().split()

        if words[0] == "open":
            app = user_input.replace("open", "").strip()
            return open_application(app)

        if words[0] == "close":
            app = user_input.replace("close", "").strip()
            return close_application(app)
    
    except Exception as e:
        return f"Error processing command: {e}"
    
    return None

last_interaction = time.time()
while True:
    user_input = input("You: ")
    
    if user_input.lower() == "opreste te":
        print("AI has stopped.")
        conn.close()
        break  
    
    system_response = process_command(user_input)
    if system_response:
        print(f"{AI_NAME}: {system_response}")
        continue
    
    ai_response = ask_ollama(user_input)
    print(f"{AI_NAME}: {ai_response}")
    save_to_memory(user_input, ai_response)
    
    last_interaction = time.time()
    time.sleep(2)