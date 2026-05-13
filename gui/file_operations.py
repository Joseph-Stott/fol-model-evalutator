from tkinter import filedialog, END

def save_model(domain_entry, constant_entry, predicates_text, formula_entry):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"),("All Files", "*.*")]
        )

        if file_path == "":
            return

        domain = domain_entry.get()
        constants = constant_entry.get()
        predicates = predicates_text.get("1.0", END).strip()
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

def load_model(domain_entry, constant_entry, predicates_text, formula_entry):
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
        
        domain_entry.delete(0, END)
        constant_entry.delete(0, END)
        predicates_text.delete("1.0", END)
        formula_entry.delete(0, END)

        domain_entry.insert(0, "\n".join(domain_lines))
        constant_entry.insert(0, "\n".join(constants_lines))
        predicates_text.insert("1.0", "\n".join(predicates_lines))
        formula_entry.insert(0, "\n".join(formula_lines))

def export_output(output_text):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"),("All Files", "*.*")]
    )

    if file_path == "":
        return

    output = output_text.get("1.0", END).strip()

    with open(file_path, "w") as file:
        file.write("Output:\n")
        file.write(output)