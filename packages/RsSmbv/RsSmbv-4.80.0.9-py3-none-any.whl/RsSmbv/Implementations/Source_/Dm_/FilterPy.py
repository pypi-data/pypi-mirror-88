from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	def get_parameter(self) -> float:
		"""[SOURce<HW>]:DM:FILTer:PARameter \n
		Sets the filter parameter of the currently selected filter type. To set the filter type, use command method RsSmbv.Source.
		Bb.Dm.FilterPy.typePy. \n
			:return: parameter: float Range: 0.05 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DM:FILTer:PARameter?')
		return Conversions.str_to_float(response)

	def set_parameter(self, parameter: float) -> None:
		"""[SOURce<HW>]:DM:FILTer:PARameter \n
		Sets the filter parameter of the currently selected filter type. To set the filter type, use command method RsSmbv.Source.
		Bb.Dm.FilterPy.typePy. \n
			:param parameter: float Range: 0.05 to 2.5
		"""
		param = Conversions.decimal_value_to_str(parameter)
		self._core.io.write(f'SOURce<HwInstance>:DM:FILTer:PARameter {param}')
