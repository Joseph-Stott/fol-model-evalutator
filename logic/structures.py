def parse_domain(domain_text):
    # Split input by commas to get potential domain elements
    parts = domain_text.split(",")
    
    cleaned_parts = []
    for part in parts:
        # Remove extra white space from each item
        item = part.strip()
        # Ignore empty entries
        if item != "":
            cleaned_parts.append(item)
            
    # Return list representing the domain       
    return cleaned_parts

def parse_constants(constants_text):
    # Dictionary to store constant mappings (name -> value)
    constants = {}
    
    # If input is empty, return empty dictionary
    if constants_text.strip() == "":
        return constants
    
    # Split input into individual constant assignments
    pairs = constants_text.split(",")
    
    for pair in pairs:
        cleaned_pair = pair.strip()
        
        # Skip empty entries
        if cleaned_pair == "":
            continue
        
        # Ensure correct format (must contain '=')
        if "=" not in cleaned_pair:
            raise ValueError(f"Invalid constant format: '{cleaned_pair}'")
        
        # Split into name and value
        name, value =  cleaned_pair.split("=", 1)
        
        name = name.strip()
        value = value.strip()
        
        # Validate both sides are non-empty
        if name == "" or  value == "":
            raise ValueError(f"Invalid constant mapping: '{cleaned_pair}'")
        
        # Store mapping
        constants[name] = value
        
    return constants

def parse_predicates(predicate_text):
    # Dictionary to store predicate definitions
    predicates = {}
    
    # Split input into lines (one predicate per line)
    lines = predicate_text.strip().splitlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if line == "":
            continue
        
        # Ensure correct format (must contain '=')
        if "=" not in line:
            raise ValueError(f"Invalid Predicate format: '{line}'")

        # Separate predicate name from its value set
        name, values_part = line.split("=", 1)
        name = name.strip()
        values_part = values_part.strip()
        
        # Ensure values are enclosed in {}
        if not values_part.startswith("{") or not values_part.endswith("}"):
            raise ValueError(f"Invalid set format in predicate: '{line}'")

        # Remove surrounding braces
        values_part = values_part[1:-1].strip()  # remove {}
        values = []

        # Handle empty set case
        if values_part == "":
            predicates[name] = {
                "arity": 1,
                "values": []
            }
            continue

        # If tuples exist, treat as higher-arity predicate
        if "(" in values_part:
            raw_tuples = values_part.split("),")

            for raw_tuple in raw_tuples:
                # Clean tuple formatting
                raw_tuple = raw_tuple.replace("(", "").replace(")", "").strip()
                parts = [p.strip() for p in raw_tuple.split(",") if p.strip() != ""]

                # Validate tuple contents
                if len(parts) == 0:
                    raise ValueError(f"Invalid tuple in predicate: '{line}'")
                
                # Enforce max arity of 3
                if len(parts) > 3:
                    raise ValueError(f"Only predicates up to arity 3 are supported: '{line}'")
                
                values.append(tuple(parts))

            # Determine arity from first tuple
            arity = len(values[0])
            
            # Ensure all tuples have consistent size
            for value in values:
                if len(value) != arity:
                    raise ValueError(f"Inconsistent tuple sizes in predicate: '{line}'")

        else:
            # Handle unary predicates (single elements)
            raw_items = values_part.split(",")

            for item in raw_items:
                item = item.strip()
                if item != "":
                    values.append((item,))

            arity = 1
        
        # Store predicate with its arity and values
        predicates[name] = {
            "arity": arity,
            "values": values
        }

    return predicates