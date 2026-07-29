from pathlib import Path


def load_css():
    css_file = Path("assets/styles.css")   # <-- plural

    if not css_file.exists():
        raise FileNotFoundError(
            f"CSS file not found: {css_file}"
        )

    with open(css_file, "r", encoding="utf-8") as file:
        css = file.read()

    return f"<style>{css}</style>"
