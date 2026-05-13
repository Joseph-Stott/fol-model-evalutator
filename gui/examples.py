import random
import tkinter as tk

EXAMPLES = [
    {
        "domain": "1,2,3",
        "constants": "",
        "predicates": "P={1}\nQ={2,3}",
        "formula": "forall x (P(x) or Q(x))"
    },
    {
        "domain": "1,2,3",
        "constants": "",
        "predicates": "P={1,3}",
        "formula": "exists x P(x)"
    },
    {
        "domain": "1,2,3",
        "constants": "a=1",
        "predicates": "P={1}\nR={(1,2),(2,3)}",
        "formula": "P(a) and R(1,2)"
    }
]

def load_random_example(domain_entry, constant_entry, predicates_text, formula_entry, output_text):
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