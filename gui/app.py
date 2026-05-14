import tkinter as tk
from logic.evaluation_service import run_evaluation
from gui.formatting import display_evaluation_output
from gui.file_operations import save_model, load_model, export_output
from gui.examples import EXAMPLES, load_random_example
from gui.history import create_history_panel, add_to_history, clear_history
from gui.widget_helpers import clear_all_fields, clear_formula

def run_app():
    root = tk.Tk()
    root.title("FOL Model Evaluator")
    root.geometry("1100x700")
    
    # Domain
    domain_label = tk.Label(root, text="Domain (comma-separated, ex. 1,2,3):")
    domain_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    domain_entry = tk.Entry(root, width=40)
    domain_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # Constants
    constant_label = tk.Label(root, text="Constants (ex. a=1, b=2):")
    constant_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    constant_entry = tk.Entry(root, width=40)
    constant_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # PREDICATES
    predicates_label = tk.Label(root, text="Predicates (ex. P={1,3}, R={(1,2),(2,3)}):")
    predicates_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

    predicates_text = tk.Text(root, height=5, width=40)
    predicates_text.grid(row=2, column=1, padx=10, pady=10)
    
    # Formula
    formula_label = tk.Label(root, text="Formula (ex. forall x P(x)):")
    formula_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    formula_entry = tk.Entry(root, width=40)
    formula_entry.grid(row=3, column=1, padx=10, pady=10)
    
    # Formula helper button row
    button_frame = tk.Frame(root)
    button_frame.grid(row=4, column=1, pady=5, sticky="w")
    
    # Output
    output_label = tk.Label(root, text="Output:")
    output_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    output_text = tk.Text(root, height=10, width=60)
    output_text.grid(row=5, column=1, padx=10, pady=10)

    output_text.tag_config("success", foreground="green")
    output_text.tag_config("failure", foreground="red")
    output_text.tag_config("error", foreground="red")
    
    evaluation_history = create_history_panel(root, formula_entry)
        
    # Evaluate button
    def evaluate():
        domain = domain_entry.get()
        constants = constant_entry.get()
        predicates = predicates_text.get("1.0", tk.END)
        formula = formula_entry.get()

        output_text.delete("1.0", tk.END)
        
        try:
            evaluation_data = run_evaluation(
                domain,
                constants,
                predicates,
                formula
            )
            
            display_evaluation_output(
                output_text,
                domain,
                evaluation_data["parsed_domain"],
                constants,
                evaluation_data["parsed_constants"],
                predicates,
                evaluation_data["parsed_predicates"],
                formula,
                evaluation_data["parsed_formula"],
                evaluation_data["trace"],
                evaluation_data["result"]
            )

            if formula.strip() != "":
                add_to_history(evaluation_history, formula, evaluation_data["result"])

        except ValueError as error:
            output_text.insert(tk.END, f"Error: {error}\n", "error")

    def create_formula_button(text, insert_text):
        tk.Button(
            button_frame,
            text=text,
            command=lambda: formula_entry.insert(tk.INSERT, insert_text)
        ).pack(side="left", padx=4)

    #Formula helper buttons
    create_formula_button("forall", "forall x ")
    create_formula_button("exists", "exists x ")
    create_formula_button("not", "not ")
    create_formula_button("and", " and ")
    create_formula_button("or", " or ")
    create_formula_button("implies", " -> ")
    create_formula_button("(", "(")
    create_formula_button(")", ")")

    tk.Button(
        button_frame,
        text="Clear Formula",
        command=lambda: clear_formula(formula_entry)
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Random Example",
        command=lambda: load_random_example(
            domain_entry,
            constant_entry,
            predicates_text,
            formula_entry,
            output_text
        )
    ).pack(side="left", padx=4)
    
    # Bottom row buttons
    bottom_button_frame = tk.Frame(root)
    bottom_button_frame.grid(row=6, column=1, pady=20)
    
    def create_bottom_button(text, command):
        tk.Button(
            bottom_button_frame,
            text=text,
            command=command
        ).pack(side="left", padx=8)

    create_bottom_button("Evaluate", evaluate)

    create_bottom_button(
        "Clear All",
        lambda: clear_all_fields(
            domain_entry,
            constant_entry,
            predicates_text,
            formula_entry, output_text
        )
    )

    create_bottom_button(
        "Save Model",
        lambda: save_model(
            domain_entry,
            constant_entry,
            predicates_text,
            formula_entry
        )
    )

    create_bottom_button(
        "Load Model",
        lambda: load_model(
            domain_entry,
            constant_entry,
            predicates_text,
            formula_entry
        )
    )
    
    create_bottom_button(
        "Export Output",
        lambda: export_output(output_text)
    )

    create_bottom_button(
        "Clear History",
        lambda: clear_history(evaluation_history)
    )

    root.mainloop()