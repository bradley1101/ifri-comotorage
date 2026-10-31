from django import forms


class StyledFormMixin:
    """Adds the CSS class used by the templates to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "check" if isinstance(field.widget, forms.CheckboxInput) else "input"
            field.widget.attrs.setdefault("class", css)
