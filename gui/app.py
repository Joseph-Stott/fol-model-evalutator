import tkinter as tk
from logic.structures import parse_domain, parse_constants, parse_predicates
from logic.formulas import parse_formula
from logic.evaluator import evaluate_formula
from gui.formatting import pretty_print
from gui.file_operations import save_model, load_model, export_output
from gui.examples import EXAMPLES
import random

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
    
    evaluation_history_frame = tk.Frame(root)
    evaluation_history_frame.grid(row=1, column=2, padx=10, pady=10, sticky="n")

    def load_formula_from_history(event):
        selected_index = evaluation_history.curselection()

        if not selected_index:
            return
    
        history_entry = evaluation_history.get(selected_index[0])
        formula_text = history_entry.split("->")[0]

        formula_entry.delete(0,tk.END)
        formula_entry.insert(0, formula_text)

    evaluation_history = tk.Listbox(
        evaluation_history_frame,
        width=45,
        height=10
    )

    evaluation_history.bind("<<ListboxSelect>>", load_formula_from_history)

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

    evaluation_history.grid(row=0, column=0, sticky="nsew")
    vertical_scroll_bar.grid(row=0, column=1, sticky="ns")
    horizontal_scroll_bar.grid(row=1, column=0, sticky="ew")
        
    # Button
    def evaluate():
        domain = domain_entry.get()
        constants = constant_entry.get()
        predicates = predicates_text.get("1.0", tk.END)
        formula = formula_entry.get()

        output_text.delete("1.0", tk.END)
        
        try:
            if domain.strip() == "":
                raise ValueError("Domain cannot be empty. Example: 1,2,3")

            if formula.strip() == "":
                raise ValueError("Formula cannot be empty. Example: forall x P(x)")
            
            parsed_domain = parse_domain(domain)
            parsed_constants = parse_constants(constants)
            parsed_predicates = parse_predicates(predicates)
            parsed_formula = parse_formula(formula)
            trace = []
            result = evaluate_formula(
                parsed_formula,
                parsed_domain,
                parsed_constants,
                parsed_predicates,
                trace
            )
            
            output_text.insert(tk.END, f"Domain: \n{domain}\n")
            output_text.insert(tk.END, f"Parsed Domain: \n{parsed_domain}\n")
            output_text.insert(tk.END, f"Constants: \n{constants}\n")
            output_text.insert(tk.END, f"Parsed Constants: \n{parsed_constants}\n")
            output_text.insert(tk.END, f"Predicates: \n{predicates}")
            output_text.insert(tk.END, "Parsed Predicates:\n")
            for name, info in parsed_predicates.items():
                arity = info["arity"]
                values = info["values"]
                output_text.insert(tk.END, f"{name} (arity {arity}): {values}\n")
            output_text.insert(tk.END, f"Formula: \n{formula}\n")
            output_text.insert(tk.END, "Parsed Formula: \n")
            output_text.insert(tk.END, pretty_print(parsed_formula) + "\n")
            output_text.insert(tk.END, "Evaluation Trace:\n")
            for step in trace:
                output_text.insert(tk.END, f"{step}\n")
            if result:
                output_text.insert(tk.END, f"Result: {result}\n", "success")
            else:
                output_text.insert(tk.END, f"Result: {result}\n", "failure")
            if formula.strip() != "":
                evaluation_history.insert(tk.END, f"{formula} -> {result}")
                evaluation_history.see(tk.END)
        except ValueError as error:
            output_text.insert(tk.END, f"Error: {error}\n", "error")
    
    def load_example():
        selected_example = random.choice(EXAMPLES)

        domain_entry.delete(0, tk.END)
        constant_entry.delete(0, tk.END)
        predicates_text.delete("1.0", tk.END)
        formula_entry.delete(0, tk.END)
        output_text.delete("1.0", tk.END)

        domain_entry.insert(0, selected_example["domain"])
        constant_entry.insert(0, selected_example["constants"])
        predicates_text.insert("1.0", selected_example["predicates"])
        formula_entry.insert(0, selected_example["formula"])

    def clear_all():
        domain_entry.delete(0, tk.END)
        constant_entry.delete(0, tk.END)
        predicates_text.delete("1.0", tk.END)
        formula_entry.delete(0, tk.END)
        output_text.delete("1.0", tk.END)
    
    def clear_history():
        evaluation_history.delete(0,tk.END)

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
        command=lambda: formula_entry.delete(0, tk.END)
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Random Example",
        command=load_example
    ).pack(side="left", padx=4)
    
    # Bottom row buttons
    bottom_button_frame = tk.Frame(root)
    bottom_button_frame.grid(row=6, column=1, pady=20)

    tk.Button(
        bottom_button_frame, 
        text="Evaluate",
        command=evaluate
    ).pack(side="left", padx=8)
    
    tk.Button(
        bottom_button_frame,
        text="Clear All",
        command=clear_all
    ).pack(side="left", padx=8)

    tk.Button(
        bottom_button_frame,
        text="Save Model",
        command=lambda: save_model(
            domain_entry,
            constant_entry,
            predicates_text,
            formula_entry
        )
    ).pack(side="left", padx=8)

    tk.Button(
        bottom_button_frame,
        text="Load Model",
        command=lambda: load_model(
            domain_entry,
            constant_entry,
            predicates_text,
            formula_entry
        )
    ).pack(side="left", padx=8)
    
    tk.Button(
        bottom_button_frame,
        text="Export Output",
        command=lambda: export_output(
            output_text
        )
    ).pack(side="left",padx=8)
    
    tk.Button(
        bottom_button_frame,
        text="Clear History",
        command=clear_history
    ).pack(side="left",padx=8)

    root.mainloop()