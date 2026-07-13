from pathlib import Path

def load_css():
    css_file = Path("assets/style.css")

    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()

    return f"<style>{css}</style>"