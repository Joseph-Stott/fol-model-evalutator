# FOL Model Evaluator

A Python/Tkinter desktop application that evaluates first-order logic formulas over a user-defined model.

## What It Does

The app allows a user to define:

- a domain
- constants
- predicates
- a first-order logic formula

It then evaluates whether the formula is true or false in that model.

This project is a model evaluator, not a theorem prover. It checks truth in a given interpretation instead of generating proofs.

## Features

- Domain input
- Constant mappings
- Unary, binary, and ternary predicates
- Logical connectives:
  - not
  - and
  - or
  - implies using `->`
- Quantifiers:
  - forall
  - exists
- Parentheses and nested formulas
- Formula helper buttons
- Load example button
- Clear controls
- Pretty-printed formula output
- Colorized results and errors
- Step-by-step evaluation trace
- Save and load model files
- Export evaluation output to a text file
- Evaluation History panel
- Clear history functionality
- Auto-scrolling evaluation history
- Scrollable evaluation history
- Clickable evaluation history entries

## Example

### Domain

    1,2,3

### Predicates

    P={1}
    Q={2,3}

### Formula

    forall x (P(x) or Q(x))

### Result

    True

## Supported Syntax

### Domain

Domain values are comma-separated:

    1,2,3

### Constants

Constants use `name=value` format:

    a=1, b=2

### Predicates

Predicates use set notation:

    P={1,3}
    R={(1,2),(2,3)}
    T={(1,2,3)}

### Formulas

Supported formula examples:

    P(1)
    not P(1)
    P(1) and Q(2)
    P(1) or Q(2)
    P(1) -> Q(2)
    forall x P(x)
    exists x (P(x) or Q(x))

## How to Run

Make sure Python is installed, then run:

    python main.py

or:

    py main.py

## Testing

Run Tests with:

    python -m unittest

## Limitations

- This is not a theorem prover.
- Quantifiers range only over domain elements.
- Predicate arity is limited to 3.
- Input syntax must follow the supported format.
- Functions and equality are not currently supported.