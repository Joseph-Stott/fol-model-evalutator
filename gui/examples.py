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