import tkinter as tk
from tkinter import simpledialog, messagebox
import pickle
import os

class OlympiadModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Olympiad Module")

        self.questions_file = "questions.pkl"
        self.results_file = "results.pkl"
        self.password = "123"  # Password for teacher access

        self.load_data()
        self.main_menu()

    def load_data(self):
        if os.path.exists(self.questions_file):
            with open(self.questions_file, 'rb') as file:
                self.questions = pickle.load(file)
        else:
            self.questions = []

        if os.path.exists(self.results_file):
            with open(self.results_file, 'rb') as file:
                self.results = pickle.load(file)
        else:
            self.results = []

    def save_data(self):
        with open(self.questions_file, 'wb') as file:
            pickle.dump(self.questions, file)
       
        with open(self.results_file, 'wb') as file:
            pickle.dump(self.results, file)

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the background color for the main window
        self.root.config(bg='lavender')

        title = tk.Label(self.root, text="Olympiad Module", font=("Helvetica", 56), pady=20, bg='lavender')
        title.pack(pady=(100,50))

        teacher_btn = tk.Button(self.root, text="Teacher", command=self.prompt_password, width=50, height=5, bg='lightblue')
        teacher_btn.pack(pady=20)

        student_btn = tk.Button(self.root, text="Student", command=self.student_menu, width=50, height=5, bg='lightgreen')
        student_btn.pack(pady=20)

    def prompt_password(self):
        password = simpledialog.askstring("Password", "Enter teacher password:", show="*")
        if password == self.password:
            self.teacher_menu()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    def teacher_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the background color for the teacher's menu
        self.root.config(bg='lightgreen')

        title = tk.Label(self.root, text="Teacher's Dashboard", font=("Helvetica", 36), pady=20, bg='lightgreen')
        title.pack(pady=(100,50))

        add_question_btn = tk.Button(self.root, text="Add Question", command=self.choose_question_type, width=50, height=5, bg='lightblue')
        add_question_btn.pack(pady=20)

        view_results_btn = tk.Button(self.root, text="View Results", command=self.view_results, width=50, height=5, bg='pink')
        view_results_btn.pack(pady=20)

        back_btn = tk.Button(self.root, text="Back", command=self.main_menu, width=50, height=5, bg='lightcoral')
        back_btn.pack(pady=20)

    def choose_question_type(self):
        question_type = simpledialog.askstring("Question Type", "Enter question type (mcq / fib / t/f):")
        if question_type == "mcq":
            self.add_question()
        elif question_type == "fib":
            self.add_fill_in_the_blank_question()
        elif question_type == "t/f":
            self.add_true_false_question()
        else:
            messagebox.showerror("Error", "Invalid question type!")

    def add_question(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        if not question:
            messagebox.showerror("Error", "Question cannot be empty!")
            return

        choices = []
        for i in range(4):
            choice = simpledialog.askstring("Input", f"Enter choice {i+1}:")
            if not choice:
                messagebox.showerror("Error", "All choices must be filled!")
                return
            choices.append(choice)

        correct_answer = simpledialog.askstring("Input", "Enter the correct answer:")
        if correct_answer and correct_answer in choices:
            self.questions.append({"question": question, "type": "multiple-choice", "choices": choices, "correct_answer": correct_answer})
            self.save_data()
            messagebox.showinfo("Success", "Question added successfully!")
        else:
            messagebox.showerror("Error", "Correct answer must be one of the choices!")

    def add_fill_in_the_blank_question(self):
        question = simpledialog.askstring("Input", "Enter the question with a blank (use _ for blank):")
        if not question:
            messagebox.showerror("Error", "Question cannot be empty!")
            return

        answer = simpledialog.askstring("Input", "Enter the correct answer:")
        if not answer:
            messagebox.showerror("Error", "Answer cannot be empty!")
            return

        self.questions.append({"question": question, "type": "fill-in-the-blanks", "correct_answer": answer})
        self.save_data()
        messagebox.showinfo("Success", "Fill-in-the-blank question added successfully!")

    def add_true_false_question(self):
        question = simpledialog.askstring("Input", "Enter the true/false question:")
        if not question:
            messagebox.showerror("Error", "Question cannot be empty!")
            return

        correct_answer = simpledialog.askstring("Input", "Enter the correct answer (true/false):")
        if correct_answer.lower() in ['true', 'false']:
            self.questions.append({"question": question, "type": "true/false", "correct_answer": correct_answer.lower()})
            self.save_data()
            messagebox.showinfo("Success", "True/False question added successfully!")
        else:
            messagebox.showerror("Error", "Correct answer must be 'true' or 'false'!")

    def view_results(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the background color for the results view
        self.root.config(bg='lightgreen')

        title = tk.Label(self.root, text="Results", font=("Helvetica", 16), pady=20, bg='lightgreen')
        title.pack()

        for result in self.results:
            result_label = tk.Label(self.root, text=f"{result['name']}: {result['score']}", font=("Helvetica", 12), bg='lavender')
            result_label.pack(pady=5)

        back_btn = tk.Button(self.root, text="Back", command=self.teacher_menu, width=30, height=2, bg='lightcoral')
        back_btn.pack(pady=10)

    def student_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the background color for the student menu
        self.root.config(bg='cyan')

        self.student_name = simpledialog.askstring("Input", "Enter your name:")
        if not self.student_name:
            self.main_menu()
            return

        self.current_question_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the background color for the question view
        self.root.config(bg='lightblue')

        if self.current_question_index >= len(self.questions):
            self.finish_quiz()
            return

        question_data = self.questions[self.current_question_index]
        question_label = tk.Label(self.root, text=question_data["question"], font=("Helvetica", 14), pady=20, bg='lightblue')
        question_label.pack()

        if question_data["type"] == "multiple-choice":
            self.selected_answer = tk.StringVar()
            for choice in question_data["choices"]:
                choice_btn = tk.Radiobutton(self.root, text=choice, variable=self.selected_answer, value=choice, font=("Helvetica", 12), bg='lightblue')
                choice_btn.pack(anchor='w')

            submit_btn = tk.Button(self.root, text="Submit", command=self.submit_answer, width=30, height=2, bg='lightgreen')
            submit_btn.pack(pady=20)

        elif question_data["type"] == "fill-in-the-blanks":
            self.answer_entry = tk.Entry(self.root, font=("Helvetica", 12))
            self.answer_entry.pack(pady=10)

            submit_btn = tk.Button(self.root, text="Submit", command=self.submit_fill_in_the_blank_answer, width=30, height=2, bg='lightgreen')
            submit_btn.pack(pady=20)

        elif question_data["type"] == "true/false":
            self.selected_answer = tk.StringVar()
            true_btn = tk.Radiobutton(self.root, text="True", variable=self.selected_answer, value="true", font=("Helvetica", 12), bg='lightblue')
            true_btn.pack(anchor='w')
            false_btn = tk.Radiobutton(self.root, text="False", variable=self.selected_answer, value="false", font=("Helvetica", 12), bg='lightblue')
            false_btn.pack(anchor='w')

            submit_btn = tk.Button(self.root, text="Submit", command=self.submit_answer, width=30, height=2, bg='lightgreen')
            submit_btn.pack(pady=20)

    def submit_answer(self):
        selected = self.selected_answer.get()
        if selected:
            question_data = self.questions[self.current_question_index]
            correct_answer = question_data["correct_answer"]

            # Debugging the answers
            print(f"Selected answer: {selected}, Correct answer: {correct_answer}")

            # Case-insensitive comparison
            if selected.lower() == correct_answer.lower():
                self.score += 1
                print(f"Score updated: {self.score}")  # Debugging the score

            self.current_question_index += 1
            self.show_question()
        else:
            messagebox.showwarning("Warning", "Please select an answer!")

    def submit_fill_in_the_blank_answer(self):
        answer = self.answer_entry.get().strip()
        if answer:
            correct_answer = self.questions[self.current_question_index]["correct_answer"]

            # Debugging the answers
            print(f"Entered answer: {answer}, Correct answer: {correct_answer}")

            if answer.lower() == correct_answer.lower():
                self.score += 1
                print(f"Score updated: {self.score}")  # Debugging the score

            self.current_question_index += 1
            self.show_question()
        else:
            messagebox.showwarning("Warning", "Please enter an answer!")

    def finish_quiz(self):
        self.results.append({"name": self.student_name, "score": self.score})
        self.save_data()
        print(f"Final score for {self.student_name}: {self.score}")  # Debugging the final score
        messagebox.showinfo("Olympiad Completed", f"Your score: {self.score}")

        self.main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = OlympiadModule(root)
    root.mainloop()


