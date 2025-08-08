from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
import random

app = Flask(__name__)

tasks = []
completed_tasks = []

def get_task(task_id):
    return next((t for t in tasks if t['id'] == task_id), None)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        text = request.form.get('text')
        mood = request.form.get('mood')
        non_living = request.form.get('nonLivingMood')  # Will be None or 'on'

        if text:
            if non_living:
                object_moods = {
                    'chair': "Feeling a bit stiff today 🪑",
                    'coffee mug': "A little empty inside ☕️",
                    'laptop': "Overworked and overheating 💻",
                    'pen': "Running out of ideas ✒️",
                    'door': "Open to possibilities 🚪",
                    'smartphone': "Constantly buzzing with excitement 📱",
                    'plant': "Feeling leafy and green 🌿",
                }
                mood_value = "Neutral mood"
                for obj in object_moods:
                    if obj in text.lower():
                        mood_value = object_moods[obj]
                        break
                else:
                    mood_value = random.choice(list(object_moods.values()))
            else:
                mood_value = mood if mood else "Neutral"

            tasks.append({'id': len(tasks) + 1, 'text': text, 'mood': mood_value})
            return redirect(url_for('view_tasks'))
        else:
            return "Invalid input", 400
    return render_template('add_task.html')

@app.route('/view')
def view_tasks():
    mood_filter = request.args.get('mood')
    if mood_filter:
        filtered = [t for t in tasks if t['mood'] == mood_filter]
    else:
        filtered = tasks
    return render_template('view_tasks.html', tasks=filtered)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task(task_id)
    if not task:
        return "Task not found", 404
    if request.method == 'POST':
        text = request.form.get('text')
        mood = request.form.get('mood')
        if text and mood:
            task['text'] = text
            task['mood'] = mood
            return redirect(url_for('view_tasks'))
        else:
            return "Invalid input", 400
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task = get_task(task_id)
    if not task:
        return "Task not found", 404
    if request.method == 'POST':
        tasks.remove(task)
        return redirect(url_for('view_tasks'))
    return render_template('delete_task.html', task=task)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/mood-stats')
def mood_stats():
    mood_counts = Counter(t['mood'] for t in tasks)
    return render_template('mood_stats.html', mood_counts=mood_counts)

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_tasks(task_id):
    task = get_task(task_id)
    if task:
        tasks.remove(task)          # Correct removal from tasks list
        completed_tasks.append(task)
    return redirect(url_for('view_tasks'))

@app.route('/completed')
def completed_tasks_page():
    return render_template('completed_tasks.html', tasks=completed_tasks)

@app.route('/profile')
def profile():
    user = {'name': 'Nandana', 'email': 'nandana@example.com'}
    return render_template('profile.html', user=user)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        prank_mode = request.form.get('prank_mode') == 'on'
        non_living_mood = request.form.get('non_living_mood') == 'on'
        print(f"Prank Mode: {prank_mode}, Non-living Mood: {non_living_mood}")
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return "Thanks for contacting us!"
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
