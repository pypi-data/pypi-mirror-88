from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gate:
	"""Gate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gate", core, parent)

	def get_count(self) -> int:
		"""[SOURce<HW>]:DME:ANALysis:GATE:COUNt \n
		No command help available \n
			:return: count: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:GATE:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:DME:ANALysis:GATE:COUNt \n
		No command help available \n
			:param count: No help available
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:GATE:COUNt {param}')
