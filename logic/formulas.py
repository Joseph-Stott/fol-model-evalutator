def parse_formula(formula_text):
    formula_text = formula_text.strip()
    
    if " and " in formula_text:
        left_text, right_text = formula_text.split(" and ", 1)
        
        return {
            "type" : "and",
            "left" : parse_formula(left_text),
            "right" : parse_formula(right_text)
        }
    
    if " or " in formula_text:
        left_text, right_text = formula_text.split(" or ", 1)
        
        return {
            "type" : "or",
            "left" : parse_formula(left_text),
            "right" : parse_formula(right_text)
        }
    
    if formula_text.startswith("not"):
        rest = formula_text[3:].strip()
        
        if rest == "":
            raise ValueError("Negation must have a formula after 'not'")
        
        return {
            "type" : "not",
            "formula" : parse_formula(rest)
        }
    
    return parse_atomic_formula(formula_text)

def parse_atomic_formula(formula_text):
    formula_text = formula_text.strip()
    
    if "(" not in formula_text or not formula_text.endswith(")"):
        raise ValueError(f"Invalid atomic formula format: '{formula_text}'")
    
    name, args_part = formula_text.split("(", 1)
    name = name.strip()
    args_part = args_part[:-1].strip()
    
    if name == "":
        raise ValueError("Predicate cannot be empty")
    
    if args_part == "":
        raise ValueError("Predicate arguments cannot be empty")
    
    args = []
    for arg in args_part.split(","):
        cleaned_arg = arg.strip()
        if cleaned_arg != "":
            args.append(cleaned_arg)
            
    if len(args) == 0:
        raise ValueError("Predicate arguments cannot be empty")
    
    if len(args) > 3:
        raise ValueError("Only formulas up to 3 arguments are supported")
    
    return {
        "type" : "predicate",
        "name" : name,
        "args" : args
    }