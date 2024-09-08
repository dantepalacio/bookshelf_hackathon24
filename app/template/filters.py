from flask import Flask


def script(text: str):
    return text.strip().removeprefix("<script>").removesuffix("</script>").strip()


def dispatch_event(type: str):
    params = "{bubbles: true}"
    return f'this.dispatchEvent(new Event("{type}", {params}))'


def add_filters(app: Flask):
    app.add_template_filter(script, "script")
    app.add_template_filter(dispatch_event, "event")
