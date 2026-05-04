import tkinter as tk
from logic.structures import parse_domain, parse_constants, parse_predicates
from logic.formulas import parse_atomic_formula, parse_formula
from logic.evaluator import evaluate_atomic_formula, evaluate_formula

def run_app():
    root = tk.Tk()
    root.title("FOL Model Evaluator")
    root.geometry("800x600")
    
    # -- Domain --
    domain_label = tk.Label(root, text="Domain (Ex. comma-separated):")
    domain_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    domain_entry = tk.Entry(root, width=40)
    domain_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # -- Constants --
    constant_label = tk.Label(root, text="Constants: (Ex. a = 1)")
    constant_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    constant_entry = tk.Entry(root, width=40)
    constant_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # --- PREDICATES ---
    predicates_label = tk.Label(root, text="Predicates: (Ex. P(x)=1,3)")
    predicates_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

    predicates_text = tk.Text(root, height=5, width=40)
    predicates_text.grid(row=2, column=1, padx=10, pady=10)
    
    # -- Formula --
    formula_label = tk.Label(root, text="Formula:")
    formula_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    formula_entry = tk.Entry(root, width=40)
    formula_entry.grid(row=3, column=1, padx=10, pady=10)
    
    # -- Output --
    output_label = tk.Label(root, text="Output:")
    output_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    output_text = tk.Text(root, height=10, width=60)
    output_text.grid(row=4, column=1, padx=10, pady=10)
    
    # -- Button -- 
    def evaluate():
        domain = domain_entry.get()
        constants = constant_entry.get()
        predicates = predicates_text.get("1.0", tk.END)
        formula = formula_entry.get()
        
        output_text.delete("1.0", tk.END)
        
        try:
            parsed_domain = parse_domain(domain)
            parsed_constants = parse_constants(constants)
            parsed_predicates = parse_predicates(predicates)
            parsed_formula = parse_formula(formula)
            result = evaluate_formula(
                parsed_formula,
                parsed_domain,
                parsed_constants,
                parsed_predicates
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
            output_text.insert(tk.END, f"Parsed Formula: \n{parsed_formula}\n")
            output_text.insert(tk.END, f"Result: {result}\n")
            
        except ValueError as error:
            output_text.insert(tk.END, f"Error: {error}\n")
    
    eval_button = tk.Button(root, text="Evaluate", command=evaluate)
    eval_button.grid(row=5, column=1, pady=20)
    
    root.mainloop()