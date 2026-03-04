import ast
from pathlib import Path

import pytest

from logic_utils import check_guess, update_score


def load_check_guess_from_app():
    app_path = Path(__file__).resolve().parent.parent / "app.py"
    source = app_path.read_text(encoding="utf-8")
    module = ast.parse(source)

    check_guess_node = next(
        node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "check_guess"
    )

    extracted_module = ast.Module(body=[check_guess_node], type_ignores=[])
    namespace = {}
    exec(compile(extracted_module, filename=str(app_path), mode="exec"), namespace)
    return namespace["check_guess"]

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_guess_negative_number_is_too_low():
    # A negative guess should be lower than a positive secret
    result = check_guess(-1, 50)
    assert result == "Too Low"


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_missed_guess_has_consistent_penalty(outcome):
    # Both non-winning outcomes should apply the same penalty regardless of attempt
    assert update_score(100, outcome, 0) == 95
    assert update_score(100, outcome, 3) == 95


def test_hint_for_too_high_asks_player_to_go_lower():
    check_guess = load_check_guess_from_app()

    outcome, message = check_guess(60, 50)

    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_hint_for_too_low_asks_player_to_go_higher():
    check_guess = load_check_guess_from_app()

    outcome, message = check_guess(40, 50)

    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"
