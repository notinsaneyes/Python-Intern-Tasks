import sqlite3
import tkinter as tk
from tkinter import messagebox

# Setting up the database
def setup_database():
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            due_date TEXT,
            priority INTEGER,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

# Task management functions
def add_task(title, description, category, due_date, priority):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, category, due_date, priority, completed)
        VALUES (?, ?, ?, ?, ?, 0)
    ''', (title, description, category, due_date, priority))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, title=None, description=None, category=None, due_date=None, priority=None, completed=None):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    updates = []
    params = []

    if title:
        updates.append("title = ?")
        params.append(title)
    if description:
        updates.append("description = ?")
        params.append(description)
    if category:
        updates.append("category = ?")
        params.append(category)
    if due_date:
        updates.append("due_date = ?")
        params.append(due_date)
    if priority is not None:
        updates.append("priority = ?")
        params.append(priority)
    if completed is not None:
        updates.append("completed = ?")
        params.append(completed)

    params.append(task_id)
    cursor.execute(f'''
        UPDATE tasks
        SET {', '.join(updates)}
        WHERE id = ?
    ''', params)
    conn.commit()
    conn.close()

def view_tasks(filter_by=None, value=None):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM tasks'
    params = []

    if filter_by:
        query += f' WHERE {filter_by} = ?'
        params.append(value)

    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def mark_task_complete(task_id):
    update_task(task_id, completed=1)

def filter_tasks_by_category(category):
    return view_tasks(filter_by='category', value=category)

def filter_tasks_by_due_date(due_date):
    return view_tasks(filter_by='due_date', value=due_date)

# Main Application Class
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        for i in range(10):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

        self.title_label = tk.Label(self.root, text="Title")
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.description_label = tk.Label(self.root, text="Description")
        self.description_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.category_label = tk.Label(self.root, text="Category")
        self.category_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        self.due_date_label = tk.Label(self.root, text="Due Date (DD-MM-YYYY)")
        self.due_date_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.due_date_entry = tk.Entry(self.root)
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        self.priority_label = tk.Label(self.root, text="Priority (1-5)")
        self.priority_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=5, column=0, padx=5, pady=5)

        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        self.update_button.grid(row=5, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=5, column=2, padx=5, pady=5)

        self.complete_button = tk.Button(self.root, text="Mark Complete", command=self.complete_task)
        self.complete_button.grid(row=6, column=0, padx=5, pady=5, columnspan=3)

        self.filter_category_label = tk.Label(self.root, text="Filter by Category")
        self.filter_category_label.grid(row=7, column=0, padx=10, pady=10, sticky='e')
        self.filter_category_entry = tk.Entry(self.root)
        self.filter_category_entry.grid(row=7, column=1, padx=10, pady=10, sticky='ew')

        self.filter_category_button = tk.Button(self.root, text="Filter", command=self.filter_by_category)
        self.filter_category_button.grid(row=7, column=2, padx=5, pady=5)

        self.filter_due_date_label = tk.Label(self.root, text="Filter by Due Date")
        self.filter_due_date_label.grid(row=8, column=0, padx=10, pady=10, sticky='e')
        self.filter_due_date_entry = tk.Entry(self.root)
        self.filter_due_date_entry.grid(row=8, column=1, padx=10, pady=10, sticky='ew')

        self.filter_due_date_button = tk.Button(self.root, text="Filter", command=self.filter_by_due_date)
        self.filter_due_date_button.grid(row=8, column=2, padx=5, pady=5)

        self.tasks_listbox = tk.Listbox(self.root, width=80, height=15)
        self.tasks_listbox.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.view_tasks()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()

        if not title or not priority:
            messagebox.showwarning("Input Error", "Title and Priority are required fields")
            return

        add_task(title, description, category, due_date, int(priority))
        self.view_tasks()

    def update_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split()[0]
            title = self.title_entry.get()
            description = self.description_entry.get()
            category = self.category_entry.get()
            due_date = self.due_date_entry.get()
            priority = self.priority_entry.get()

            update_task(
                task_id,
                title if title else None,
                description if description else None,
                category if category else None,
                due_date if due_date else None,
                int(priority) if priority else None
            )
            self.view_tasks()
        except:
            messagebox.showwarning("Selection Error", "Select a task to update")

    def delete_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split()[0]
            delete_task(task_id)
            self.view_tasks()
        except:
            messagebox.showwarning("Selection Error", "Select a task to delete")

    def complete_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split()[0]
            mark_task_complete(task_id)
            self.view_tasks()
        except:
            messagebox.showwarning("Selection Error", "Select a task to mark as complete")

    def filter_by_category(self):
        category = self.filter_category_entry.get()
        tasks = filter_tasks_by_category(category)
        self.display_tasks(tasks)

    def filter_by_due_date(self):
        due_date = self.filter_due_date_entry.get()
        tasks = filter_tasks_by_due_date(due_date)
        self.display_tasks(tasks)

    def view_tasks(self):
        tasks = view_tasks()
        self.display_tasks(tasks)

    def display_tasks(self, tasks):
        self.tasks_listbox.delete(0, tk.END)
        for task in tasks:
            task_str = f"{task[0]} - Title: {task[1]}, Description: {task[2]}, Category: {task[3]}, Due: {task[4]}, Priority: {task[5]}, Completed: {'Yes' if task[6] else 'No'}"
            self.tasks_listbox.insert(tk.END, task_str)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
