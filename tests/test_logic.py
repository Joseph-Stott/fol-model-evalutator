import unittest
from logic.structures import parse_domain, parse_constants, parse_predicates
from logic.formulas import parse_formula
from logic.evaluator import evaluate_formula
import textwrap

class TestFOLModelEvaluator(unittest.TestCase):

    def setUp(self):
        # setUp runs before each test so every test starts with the same model
        self.domain = parse_domain("1,2,3")
        self.constants = parse_constants("")

        # textwrap.dedent lets the predicate input stay visually indented in the code
        # while removing extra spaces before it is parsed
        self.predicates = parse_predicates(
            textwrap.dedent("""
            P={1}
            Q={2,3}
            R={(1,2),(2,3)}
            """)
        )
        
    def evaluate(self, formula_text):
        # Helper method to avoid repeating parse/evaluate logic in every test
        parsed_formula = parse_formula(formula_text)

        return evaluate_formula(
            parsed_formula,
            self.domain,
            self.constants,
            self.predicates
        )
    
    def test_atomic_true(self):
        # P is defined as true for 1
        self.assertTrue(self.evaluate("P(1)"))

    def test_atomic_false(self):
        # P is not defined as true for 2
        self.assertFalse(self.evaluate("P(2)"))

    def test_and(self):
        # Both sides are true
        self.assertTrue(self.evaluate("P(1) and Q(2)"))

    def test_or(self):
        # Left side is false, but right side is true
        self.assertTrue(self.evaluate("P(2) or Q(2)"))

    def test_not(self):
        # P(2) is false, so not P(2) is true
        self.assertTrue(self.evaluate("not P(2)"))

    def test_implies_false(self):
        # Implication is false only when the left side is true and the right side is false
        self.assertFalse(self.evaluate("P(1) -> Q(1)"))

    def test_forall(self):
        # Every domain value satisfies P(x) or Q(x)
        self.assertTrue(self.evaluate("forall x (P(x) or Q(x))"))

    def test_exists(self):
        # At least one domain value satisfies P(x)
        self.assertTrue(self.evaluate("exists x P(x)"))

    def test_binary_predicate(self):
        # R is a binary predicate containing the tuple (1,2)
        self.assertTrue(self.evaluate("R(1,2)"))


if __name__ == "__main__":
    unittest.main()