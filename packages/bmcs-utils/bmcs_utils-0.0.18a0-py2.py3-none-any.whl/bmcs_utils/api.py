
from bmcs_utils.interactive_window import InteractiveWindow
from bmcs_utils.interactive_model import InteractiveModel
from bmcs_utils.view import View
from bmcs_utils.item import Item
from bmcs_utils.mpl_utils import mpl_align_xaxis, mpl_align_yaxis
from bmcs_utils.symb_expr import SymbExpr, InjectSymbExpr
from bmcs_utils.trait_types import Int, Float, Bool, Button, Range, Progress
from bmcs_utils.editors import \
    IntEditor, BoolEditor, FloatEditor, FloatRangeEditor, ProgressEditor, \
    ButtonEditor

# TODO [RC]: Define a protocol for the specification of assigned todos - nicknames
# TODO [RC]: check if ipykernal installation is necessary