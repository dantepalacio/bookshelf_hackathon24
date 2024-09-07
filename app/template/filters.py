from flask import Flask


def script(text: str):
    return text.strip().removeprefix("<script>").removesuffix("</script>").strip()


def add_filters(app: Flask):
    app.add_template_filter(script, "script")
