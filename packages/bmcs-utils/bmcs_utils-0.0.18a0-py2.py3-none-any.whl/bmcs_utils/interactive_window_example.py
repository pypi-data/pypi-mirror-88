
from bmcs_utils.interactive_window import InteractiveWindow
from bmcs_utils.interactive_model import InteractiveModel
from bmcs_utils.view import View
from bmcs_utils.item import Item


from bmcs_utils.trait_types import \
    Float, FloatEditor

class Model(InteractiveModel):
    a = Float(20)
    b = Float(80)

    ipw_view = View(
        Item('a', latex='a', editor=FloatEditor()),
        Item('b', latex='b')
    )


m = Model()

ii = InteractiveWindow(m)

print(
    ii.ipw_model_tabs[0].get_editors()
)
