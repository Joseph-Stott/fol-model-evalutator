def parse_domain(domain_text):
    parts = domain_text.split(",")
    
    cleaned_parts = []
    for part in parts:
        item = part.strip()
        if item != "":
            cleaned_parts.append(item)
    return cleaned_parts

def parse_constants(constants_text):
    constants = {}
    
    if constants_text.strip() == "":
        return constants
    
    pairs = constants_text.split(",")
    
    for pair in pairs:
        cleaned_pair = pair.strip()
        
        if cleaned_pair == "":
            continue
        
        if "=" not in cleaned_pair:
            raise ValueError(f"Invalid constant format: '{cleaned_pair}'")
        
        name, value =  cleaned_pair.split("=", 1)
        
        name = name.strip()
        value = value.strip()
        
        if name == "" or  value == "":
            raise ValueError(f"Invalid constant mapping: '{cleaned_pair}'")
        
        constants[name] = value
        
    return constants

def parse_predicates(predicate_text):
    predicates = {}
    
    lines = predicate_text.strip().splitlines()
    
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        
        if "=" not in line:
            raise ValueError(f"Invalid Predicate format: '{line}'")

        name, values_part = line.split("=", 1)
        name = name.strip()
        values_part = values_part.strip()
        
        if not values_part.startswith("{") or not values_part.endswith("}"):
            raise ValueError(f"Invalid set format in predicate: '{line}'")

        values_part = values_part[1:-1].strip()  # remove {}
        values = []

        if values_part == "":
            predicates[name] = {
                "arity": 1,
                "values": []
            }
            continue

        # Handle tuples (binary predicates)
        if "(" in values_part:
            raw_tuples = values_part.split("),")

            for raw_tuple in raw_tuples:
                raw_tuple = raw_tuple.replace("(", "").replace(")", "").strip()
                parts = [p.strip() for p in raw_tuple.split(",") if p.strip() != ""]

                if len(parts) == 0:
                    raise ValueError(f"Invalid tuple in predicate: '{line}'")
                
                if len(parts) > 3:
                    raise ValueError(f"Only predicates up to arity 3 are supported: '{line}'")
                
                values.append(tuple(parts))

            arity = len(values[0])
            
            for value in values:
                if len(value) != arity:
                    raise ValueError(f"Inconsistent tuple sizes in predicate: '{line}'")

        else:
            # unary predicates
            raw_items = values_part.split(",")

            for item in raw_items:
                item = item.strip()
                if item != "":
                    values.append((item,))

            arity = 1

        predicates[name] = {
            "arity": arity,
            "values": values
        }

    return predicates
    
    