from glue.core.data import Data
from glue.core.state import _save_data_4, _load_data_4, saver, loader

__all__ = ["PhaseData"]

class PhaseData(Data):
    def __init__(self, df, **kwargs):
        super().__init__(**kwargs)

        self.style.color = "#ff0000"

        self.add_component(df.index, "phase")
        for c in df.columns:
            self.add_component(df[c], str(c))

@saver(PhaseData)
def _save_phase_data(data, context):
    return _save_data_4(data, context)

@loader(PhaseData)
def _load_phase_data(rec, context):
    data = _load_data_4(rec, context) # Return Data not PhaseData object
