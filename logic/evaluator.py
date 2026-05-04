def evaluate_formula(parsed_formula, domain, constants, predicates):
    formula_type = parsed_formula["type"]
    
    # Case 1: Atomic predicate
    if formula_type == "predicate":
        return evaluate_atomic_formula(parsed_formula, constants, predicates)
    
    # Case 2: Negation
    if formula_type == "not":
        inner_result = evaluate_formula(
            parsed_formula["formula"],
            domain,
            constants,
            predicates
        )
        return not inner_result
    
    # Case 3: AND
    if formula_type == "and":
        left_result = evaluate_formula(
            parsed_formula["left"],
            domain,
            constants,
            predicates
        )
        
        right_result = evaluate_formula(
            parsed_formula["right"],
            domain,
            constants,
            predicates
        )
        
        return left_result and right_result
    
    # Case 4: OR
    if formula_type == "or":
        left_result = evaluate_formula(
            parsed_formula["left"],
            domain,
            constants,
            predicates
        )
        right_result = evaluate_formula(
            parsed_formula["right"],
            domain,
            constants,
            predicates
        )
        return left_result or right_result
    
    # Case 5: Implies
    if formula_type == "implies":
        left_result = evaluate_formula(
            parsed_formula["left"],
            domain,
            constants,
            predicates
        )
        right_result = evaluate_formula(
            parsed_formula["right"],
            domain,
            constants,
            predicates
        )
        
        return (not left_result) or right_result
    
    # Case 6: For all
    if formula_type == "forall":
        variable = parsed_formula["var"]
        inner_formula = parsed_formula["formula"]
    
        for element in domain:
            new_constants = constants.copy()
            new_constants[variable] = element
            
            if not evaluate_formula(inner_formula, domain, new_constants, predicates):
                return False
        
        return True
    
    # Case 7: Exists
    if formula_type == "exists":
        variable = parsed_formula["var"]
        inner_formula = parsed_formula["formula"]
        
        for element in domain:
            new_constants = constants.copy()
            new_constants[variable] = element
            
            if evaluate_formula(inner_formula, domain, new_constants, predicates):
                return True
        
        return False
    
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