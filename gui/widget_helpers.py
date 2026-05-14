import tkinter as tk

def clear_all_fields(domain_entry, constant_entry, predicates_text, formula_entry, output_text):
        domain_entry.delete(0, tk.END)
        constant_entry.delete(0, tk.END)
        predicates_text.delete("1.0", tk.END)
        formula_entry.delete(0, tk.END)
        output_text.delete("1.0", tk.END)

def clear_formula(formula_entry):
        formula_entry.delete(0, tk.END)