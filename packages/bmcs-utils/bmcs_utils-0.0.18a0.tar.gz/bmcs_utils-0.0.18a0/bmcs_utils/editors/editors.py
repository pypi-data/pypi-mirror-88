import traits.api as tr
import ipywidgets as ipw


class EditorFactory(tr.HasTraits):
    name = tr.Str
    model = tr.WeakRef
    tooltip = tr.Str
    value = tr.Any
    trait = tr.Trait
    label = tr.Str
    disabled = tr.Bool(False)
    ui_pane = tr.WeakRef


class FloatEditor(EditorFactory):
    def render(self):
        return ipw.FloatText(description=self.label, value=self.value,
                             tooltip=self.tooltip, disabled=self.disabled)


class IntEditor(EditorFactory):
    def render(self):
        return ipw.IntText(description=self.label, value=self.value,
                           tooltip=self.tooltip, disabled=self.disabled)


class BoolEditor(EditorFactory):
    def render(self):
        return ipw.Checkbox(description=self.label, value=self.value,
                            tooltip=self.tooltip, disabled=self.disabled)


class FloatRangeEditor(EditorFactory):
    low = tr.Float
    high = tr.Float
    low_name = tr.Str
    high_name = tr.Str
    n_steps = tr.Int(20)
    n_steps_name = tr.Str
    continuous_update = tr.Bool(False)

    def render(self):
        if self.low_name:
            self.low = getattr(self.model, str(self.low_name))
        if self.high_name:
            self.high = getattr(self.model, str(self.high_name))
        if self.n_steps_name:
            self.n_steps = getattr(self.model, str(self.n_steps_name))
        step = (self.high - self.low) / self.n_steps
        return ipw.FloatSlider(
            value=self.value,
            min=self.low,
            max=self.high,
            step=step,
            tooltip=self.tooltip,
            continuous_update=self.continuous_update,
            description=self.label,
            disabled=self.disabled
        )


class ButtonEditor(EditorFactory):
    icon = tr.Str('check')

    def render(self):
        button = ipw.Button(
            description=self.label,
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip=self.tooltip,
            icon=self.icon  # (FontAwesome names without the `fa-` prefix)
        )

        def button_clicked(change):
            setattr(self.model, self.name, True)

        button.on_click(button_clicked)
        return button
