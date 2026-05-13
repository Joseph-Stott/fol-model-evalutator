from logic.structures import (parse_domain, parse_constants, parse_predicates)
from logic.formulas import parse_formula
from logic.evaluator import evaluate_formula

def run_evaluation(domain, constants, predicates, formula):
    if domain.strip() == "":
        raise ValueError("Domain cannot be empty. Example: 1,2,3")

    if formula.strip() == "":
        raise ValueError("Formula cannot be empty. Example: forall x P(x)")
    
    parsed_domain = parse_domain(domain)
    parsed_constants = parse_constants(constants)
    parsed_predicates = parse_predicates(predicates)
    parsed_formula = parse_formula(formula)
    trace = []
    result = evaluate_formula(
        parsed_formula,
        parsed_domain,
        parsed_constants,
        parsed_predicates,
        trace
    )
    
    return {
        "parsed_domain": parsed_domain,
        "parsed_constants": parsed_constants,
        "parsed_predicates": parsed_predicates,
        "parsed_formula": parsed_formula,
        "trace": trace,
        "result": result
    }
