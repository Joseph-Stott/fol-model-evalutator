import tkinter as tk

def create_history_panel(root, formula_entry):
        evaluation_history_frame = tk.Frame(root)
        evaluation_history_frame.grid(row=1, column=2, padx=10, pady=10, sticky="n")

        def load_history_selection(event):
            selected_index = evaluation_history.curselection()

            if not selected_index:
                return

            history_entry = evaluation_history.get(selected_index[0])
            formula_text = history_entry.split("->")[0].strip()

            formula_entry.delete(0, tk.END)
            formula_entry.insert(0, formula_text)

        evaluation_history = tk.Listbox(
            evaluation_history_frame,
            width=45,
            height=10
        )

        evaluation_history.bind("<<ListboxSelect>>", load_history_selection)

        vertical_scroll_bar = tk.Scrollbar(
            evaluation_history_frame,
            orient="vertical",
            command=evaluation_history.yview
        )

        horizontal_scroll_bar = tk.Scrollbar(
            evaluation_history_frame,
            orient="horizontal",
            command=evaluation_history.xview
        )

        evaluation_history.config(
            yscrollcommand=vertical_scroll_bar.set,
            xscrollcommand=horizontal_scroll_bar.set
        )

        evaluation_history.grid(row=0, column=0, sticky="nsew")
        vertical_scroll_bar.grid(row=0, column=1, sticky="ns")
        horizontal_scroll_bar.grid(row=1, column=0, sticky="ew")

        return evaluation_history

def add_to_history(evaluation_history, formula, result):
    evaluation_history.insert(tk.END, f"{formula} -> {result}")
    evaluation_history.see(tk.END)

def clear_history(evaluation_history):
    evaluation_history.delete(0, tk.END)