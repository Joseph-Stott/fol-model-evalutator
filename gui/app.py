import tkinter as tk
from tkinter import filedialog
from logic.structures import parse_domain, parse_constants, parse_predicates
from logic.formulas import parse_formula
from logic.evaluator import evaluate_formula

# Pretty Print
def pretty_print(formula, indent=0):
    space = "  " * indent
    
    if formula["type"] == "predicate":
        return space + f"{formula['name']}({', '.join(formula['args'])})"
    
    if formula["type"] == "not":
        return space + "NOT\n" + pretty_print(formula["formula"], indent+1)
    
    if formula["type"] in ["and", "or", "implies"]:
        return(
            space + formula["type"].upper() + "\n" +
            pretty_print(formula["left"], indent+1) + "\n" +
            pretty_print(formula["right"], indent+1)
        )
    
    if formula["type"] in ["forall", "exists"]:
        return(
            space + f"{formula['type'].upper()} {formula['var']}\n" +
            pretty_print(formula["formula"], indent+1)
        )
        
    return space + str(formula)

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
        domain_entry.delete(0, tk.END)
        constant_entry.delete(0, tk.END)
        predicates_text.delete("1.0", tk.END)
        formula_entry.delete(0, tk.END)
        output_text.delete("1.0", tk.END)

        domain_entry.insert(0, "1,2,3")
        predicates_text.insert("1.0", "P={1}\nQ={2,3}")
        formula_entry.insert(0, "forall x (P(x) or Q(x))")


    def clear_all():
        domain_entry.delete(0, tk.END)
        constant_entry.delete(0, tk.END)
        predicates_text.delete("1.0", tk.END)
        formula_entry.delete(0, tk.END)
        output_text.delete("1.0", tk.END)

    def save_model():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"),("All Files", "*.*")]
        )

        if file_path == "":
            return

        domain = domain_entry.get()
        constants = constant_entry.get()
        predicates = predicates_text.get("1.0", tk.END).strip()
        formula = formula_entry.get()

        with open(file_path, "w") as file:
            file.write("Domain:\n")
            file.write(domain + "\n\n")

            file.write("Constants:\n")
            file.write(constants + "\n\n")

            file.write("Predicates:\n")
            file.write(predicates + "\n\n")

            file.write("Formula:\n")
            file.write(formula + "\n")
    
    def load_model():
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"),("All Files", "*.*")]
        )

        if file_path == "":
            return
        
        domain_lines = []
        constants_lines = []
        predicates_lines = []
        formula_lines = []

        current_section = None

        with open(file_path, "r") as file:
            for line in file:
                cleaned_line = line.strip()

                if cleaned_line.lower() == "domain:":
                    current_section = "domain"
                    continue
                elif cleaned_line.lower() == "constants:":
                    current_section = "constants"
                    continue
                elif cleaned_line.lower() == "predicates:":
                    current_section = "predicates"
                    continue
                elif cleaned_line.lower() == "formula:":
                    current_section = "formula"
                    continue

                if current_section == "domain" and cleaned_line != "":
                    domain_lines.append(cleaned_line)
                elif current_section == "constants" and cleaned_line != "":
                    constants_lines.append(cleaned_line)
                elif current_section == "predicates" and cleaned_line != "":
                    predicates_lines.append(cleaned_line)
                elif current_section == "formula" and cleaned_line != "":
                    formula_lines.append(cleaned_line)
        
        domain_entry.delete(0, tk.END)
        constant_entry.delete(0, tk.END)
        predicates_text.delete("1.0", tk.END)
        formula_entry.delete(0, tk.END)

        domain_entry.insert(0, "\n".join(domain_lines))
        constant_entry.insert(0, "\n".join(constants_lines))
        predicates_text.insert("1.0", "\n".join(predicates_lines))
        formula_entry.insert(0, "\n".join(formula_lines))

    def export_output():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"),("All Files", "*.*")]
        )

        if file_path == "":
            return

        output = output_text.get("1.0", tk.END).strip()

        with open(file_path, "w") as file:
            file.write("Output:\n")
            file.write(output)
    
    def clear_history():
        evaluation_history.delete(0,tk.END)


    #Formula helper buttons
    tk.Button(
        button_frame,
        text="forall",
        command=lambda: formula_entry.insert(tk.INSERT, "forall x ")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="exists",
        command=lambda: formula_entry.insert(tk.INSERT, "exists x ")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="not",
        command=lambda: formula_entry.insert(tk.INSERT, "not ")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="and",
        command=lambda: formula_entry.insert(tk.INSERT, " and ")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="or",
        command=lambda: formula_entry.insert(tk.INSERT, " or ")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="implies",
        command=lambda: formula_entry.insert(tk.INSERT, " -> ")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="(",
        command=lambda: formula_entry.insert(tk.INSERT, "(")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text=")",
        command=lambda: formula_entry.insert(tk.INSERT, ")")
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Clear Formula",
        command=lambda: formula_entry.delete(0, tk.END)
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Load Example",
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
        text="Save",
        command=save_model
    ).pack(side="left", padx=8)

    tk.Button(
        bottom_button_frame,
        text="Load",
        command=load_model
    ).pack(side="left", padx=8)
    
    tk.Button(
        bottom_button_frame,
        text="Export Output",
        command=export_output
    ).pack(side="left",padx=8)
    
    tk.Button(
        bottom_button_frame,
        text="Clear History",
        command=clear_history
    ).pack(side="left",padx=8)

    root.mainloop()