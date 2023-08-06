from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ask:
	"""Ask commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ask", core, parent)

	def get_depth(self) -> float:
		"""[SOURce<HW>]:BB:DM:ASK:DEPTh \n
		Sets the ASK modulation depth for modulation type ASK. \n
			:return: depth: float Range: 0 to 100, Unit: PCT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:ASK:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""[SOURce<HW>]:BB:DM:ASK:DEPTh \n
		Sets the ASK modulation depth for modulation type ASK. \n
			:param depth: float Range: 0 to 100, Unit: PCT
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:ASK:DEPTh {param}')
