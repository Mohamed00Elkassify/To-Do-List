import mysql.connector

class To_do_list:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='obie9090',
            database='todolist')

        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT FALSE)
                            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS completed_tasks (
                task TEXT)
                            ''')

    def add_tasks(self, task):
        self.cursor.execute("INSERT INTO tasks (description) VALUES (%s)", (task,))
        self.connection.commit()
        print("Task added successfully")
        print("="*50)
    
    def show_tasks(self):
        self.cursor.execute("SELECT * FROM tasks WHERE completed = FALSE")
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            print("No tasks to show")
            print("="*50)
        else:
            print("Your tasks are:")
            for i, row in enumerate(rows, start = 1):
                print(f"{i}-{row[1]}")
            print("="*20)
    
    def mark_as_done(self):
        self.cursor.execute("SELECT * FROM tasks WHERE completed = FALSE")
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            print("No tasks to mark as done")
            print("="*50)
        else:
            print("Your tasks are:")
            for i, row in enumerate(rows, start=1):
                print(f"{i}-{row[1]}")
            print("="*50)
            choice = int(input("Enter the number of the task you want to mark as done: ")) - 1
            if 0 <= choice < len(rows):
                self.cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (rows[choice][0],))
                self.connection.commit()
                self.cursor.execute("INSERT INTO completed_tasks (task) SELECT description FROM tasks WHERE id = %s", (rows[choice][0],))
                self.connection.commit()
                print("Task marked as done and moved to completed tasks.")
                print("="*50)
            else:
                print("Invalid choice")
                print("="*50)
    
    def show_completed_tasks(self):
        self.cursor.execute("SELECT * FROM completed_tasks")
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            print("No completed tasks to show")
            print("="*50)
        else:
            print("Your completed tasks are:")
            for i, row in enumerate(rows, start = 1):
                print(f"{i}-{row[0]}")
            print("="*50)
    
    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    to_do_list = To_do_list()
    while True:
        print("\nTo do list")
        print("="*10)
        print("1-add a task✍️")
        print("2-Show tasks📄")
        print("3-Mark as done✔️")
        print("4-Show completed tasks📋")
        print("5-Exit🔚")

        choice = int(input("Enter your choice: "))
        print("="*50)
        if choice == 1:
            task = input("Enter your task: ")
            to_do_list.add_tasks(task)
        elif choice == 2:
            to_do_list.show_tasks()
        elif choice == 3:
            to_do_list.mark_as_done()
        elif choice == 4:
            to_do_list.show_completed_tasks()
        elif choice == 5:
            to_do_list.close()
            print("To-do list application closed.")
            break
        else:
            print("Invalid choice. Please try again.")