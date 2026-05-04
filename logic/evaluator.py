def evaluate_formula(parsed_formula, constants, predicates):
    formula_type = parsed_formula["type"]
    
    # Case 1: Atomic predicate
    if formula_type == "predicate":
        return evaluate_atomic_formula(parsed_formula, constants, predicates)
    
    # Case 2: Negation
    if formula_type == "not":
        inner_result = evaluate_formula(
            parsed_formula["formula"],
            constants,
            predicates
        )
        return not inner_result
    
    raise ValueError(f"Unknown formula type: '{formula_type}'")
    
    
def evaluate_atomic_formula(parsed_formula, constants, predicates):
    name = parsed_formula["name"]
    args = parsed_formula["args"]
    
    # Step 1: Resolve constants 
    resolved_args = []
    
    for arg in args:
        if arg in constants:
            resolved_args.append(constants[arg])
        else:
            resolved_args.append(arg)
            
    # Step 2: Convert to tuple
    args_tuple = tuple(resolved_args)
    
    # Step 3: Check predicate exists
    if name not in predicates:
        raise ValueError(f"Predicate '{name}' is not defined")
    
    predicate_info = predicates[name]
    
    # Step 4: Check arity matches
    if len(args_tuple) != predicate_info["arity"]:
        raise ValueError(f"Arity mismatch for predicate '{name}'")
    
    # Step 5: Check membership
    return args_tuple in predicate_info["values"]