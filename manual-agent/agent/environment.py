"""
Agent Environment: Verified information about Code Smells.

Sources of facts:
- Martin Fowler, "Refactoring: Improving the Design of Existing Code",
  2nd Edition, 2018.
- Martin Fowler, "Refactoring" — каталог Code Smells:
  https://refactoring.com/catalog/
- Joshua Kerievsky, "Refactoring to Patterns", 2004.
"""

CODE_SMELLS: dict[str, str] = {
    "duplicated-code": (
        "Duplicated Code: identical or very similar code fragments appear in multiple "
        "places. Changes must be repeated in each fragment. Refactoring approach: "
        "Extract Function or Consolidate Duplicate Conditional Fragments."
    ),
    "long-method": (
        "Long Method: a method contains too much logic and performs several distinct "
        "operations, making it harder to read, test, and modify. Refactoring approach: "
        "Extract Function or Replace Temp with Query."
    ),
    "large-class": (
        "Large Class: a class contains too many fields, methods, or responsibilities. "
        "This makes its code difficult to understand and maintain. Refactoring "
        "direction: Extract Class or Extract Subclass."
    ),
    "feature-envy": (
        "Feature Envy: a method uses data and methods from another class more frequently "
        "than those of its own class. This may indicate that the behavior is poorly "
        "placed. Refactoring direction: Move Function."
    ),
    "shotgun-surgery": (
        "Shotgun Surgery (scattered changes): a single change in requirements "
        "necessitates edits across many different classes or methods. This increases "
        "the risk of missing a necessary change. Refactoring direction: use Move "
        "Function or Move Field to consolidate related behavior in a single location."
    ),
    "data-clumps": (
        "Data Clumps: identical groups of parameters or fields frequently appear "
        "together in various parts of a program. This may indicate that the data should "
        "be combined into a separate object. Refactoring approach: Introduce Parameter "
        "Object or Extract Class."
    ),
    "primitive-obsession": (
        "Primitive Obsession (overuse of primitive types): primitive types, such as "
        "strings and numbers, are used to represent more complex domain concepts. "
        "Refactoring approach: Replace Primitive with Object or Introduce Value Object."
    ),
}

NOT_FOUND = "NOT_FOUND"


def normalize_name(name: str) -> str:
    """Normalizes the "Code Smell" name for search purposes."""
    return name.strip().lower().replace(" ", "-").replace("_", "-")


def lookup_code_smell(name: str) -> str:
    """
    Returns reference information about a specific Code Smell.

    Supports the names: duplicated-code, long-method, large-class,
    feature-envy, shotgun-surgery, data-clumps, and
    primitive-obsession.

    Args:
        name: The name of the code smell, e.g., "Long Method".

    Returns:
        The identifier and description of the Code Smell, or a NOT_FOUND message.
    """
    key = normalize_name(name)

    if key not in CODE_SMELLS:
        return f"{NOT_FOUND}: no verified information about '{name}'."

    return f"{key}: {CODE_SMELLS[key]}"


def list_code_smells() -> str:
    """Returns a sorted list of known Code Smells."""
    return ", ".join(sorted(CODE_SMELLS))
