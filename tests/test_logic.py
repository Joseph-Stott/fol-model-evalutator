import unittest
from logic.structures import parse_domain, parse_constants, parse_predicates
from logic.formulas import parse_formula
from logic.evaluator import evaluate_formula
import textwrap

class TestFOLModelEvaluator(unittest.TestCase):

    def setUp(self):
        self.domain = parse_domain("1,2,3")
        self.constants = parse_constants("")
        self.predicates = parse_predicates(
            textwrap.dedent("""
            P={1}
            Q={2,3}
            R={(1,2),(2,3)}
            """)
        )
        
    def evaluate(self, formula_text):
        parsed_formula = parse_formula(formula_text)
        return evaluate_formula(
            parsed_formula,
            self.domain,
            self.constants,
            self.predicates
        )
    
    def test_atomic_true(self):
        self.assertTrue(self.evaluate("P(1)"))

    def test_atomic_false(self):
        self.assertFalse(self.evaluate("P(2)"))

    def test_and(self):
        self.assertTrue(self.evaluate("P(1) and Q(2)"))

    def test_or(self):
        self.assertTrue(self.evaluate("P(2) or Q(2)"))

    def test_not(self):
        self.assertTrue(self.evaluate("not P(2)"))

    def test_implies_false(self):
        self.assertFalse(self.evaluate("P(1) -> Q(1)"))

    def test_forall(self):
        self.assertTrue(self.evaluate("forall x (P(x) or Q(x))"))

    def test_exists(self):
        self.assertTrue(self.evaluate("exists x P(x)"))

    def test_binary_predicate(self):
        self.assertTrue(self.evaluate("R(1,2)"))


if __name__ == "__main__":
    unittest.main()