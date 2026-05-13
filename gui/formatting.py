import tkinter as tk

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

def display_evaluation_output(
        output_text,
        domain,
        parsed_domain,
        constants,
        parsed_constants,
        predicates,
        parsed_predicates, 
        formula,
        parsed_formula,
        trace,
        result
    ):
    output_text.insert(tk.END, f"Domain:\n{domain}\n")
    output_text.insert(tk.END, f"Parsed Domain:\n{parsed_domain}\n")
    output_text.insert(tk.END, f"Constants:\n{constants}\n")
    output_text.insert(tk.END, f"Parsed Constants:\n{parsed_constants}\n")
    output_text.insert(tk.END, f"Predicates:\n{predicates}\n")
    output_text.insert(tk.END, f"Parsed Predicates:\n{parsed_predicates}\n")

    for name, info in parsed_predicates.items():
        arity = info["arity"]
        values = info["values"]
        output_text.insert(tk.END, f"{name} (arity {arity}): {values}\n")

    output_text.insert(tk.END, f"Formula:\n{formula}\n")
    output_text.insert(tk.END, f"Parsed Formula:\n")
    output_text.insert(tk.END, pretty_print(parsed_formula) + "\n")

    output_text.insert(tk.END, "Evaluation Trace:\n")
    for step in trace:
        output_text.insert(tk.END, f"{step}\n")

    if result:
        output_text.insert(tk.END, f"Result: {result}\n", "success")
    else:
        output_text.insert(tk.END, f"Result: {result}\n", "failure")