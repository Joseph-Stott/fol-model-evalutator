def split_top_level(formula_text, operator):
    count = 0
    
    for i in range(len(formula_text)):
        char = formula_text[i]
        
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
                
        if count == 0 and formula_text.startswith(operator, i):
            left = formula_text[:i].strip()
            right = formula_text[i + len(operator):].strip()
            return left, right
        
    return None

def parse_formula(formula_text):
    formula_text = formula_text.strip()
    
    # Handle outer parentheses only if they wrap the whole formula
    if formula_text.startswith("(") and formula_text.endswith(")"):
        count = 0
        wraps_whole_formula = True

        for i, char in enumerate(formula_text):
            if char == "(":
                count += 1
            elif char == ")":
                count -= 1

            if count == 0 and i != len(formula_text) - 1:
                wraps_whole_formula = False
                break

        if wraps_whole_formula:
            return parse_formula(formula_text[1:-1].strip())
    
    if formula_text.startswith("forall"):
        parts = formula_text.split(" ", 2)
        
        if len(parts) < 3:
            raise ValueError("Invalid forall format")
        
        _, var, rest = parts
        
        return {
            "type" : "forall",
            "var" : var.strip(),
            "formula" : parse_formula(rest.strip())
        }
    
    if formula_text.startswith("exists"):
        parts = formula_text.split(" ", 2)
        
        if len(parts) < 3:
            raise ValueError("Invalid exists format")
        
        _, var, rest = parts
        
        return {
            "type" : "exists",
            "var" : var.strip(),
            "formula" : parse_formula(rest.strip())
        }
    
    and_split = split_top_level(formula_text, " and ")
    if and_split:
        left_text, right_text = and_split
        
        return {
            "type" : "and",
            "left" : parse_formula(left_text),
            "right" : parse_formula(right_text)
        }
    
    or_split = split_top_level(formula_text, " or ")
    if or_split:
        left_text, right_text = or_split
        
        return {
            "type" : "or",
            "left" : parse_formula(left_text),
            "right" : parse_formula(right_text)
        }
    
    implies_split = split_top_level(formula_text, " -> ")
    if implies_split:
        left_text, right_text = implies_split
        
        return {
            "type" : "implies",
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