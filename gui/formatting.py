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
