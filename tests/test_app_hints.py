import ast
from pathlib import Path


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


def test_hint_for_too_high_in_typeerror_fallback_asks_player_to_go_lower():
    check_guess = load_check_guess_from_app()

    outcome, message = check_guess(60, "50")

    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_hint_for_too_low_in_typeerror_fallback_asks_player_to_go_higher():
    check_guess = load_check_guess_from_app()

    outcome, message = check_guess(40, "50")

    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"
