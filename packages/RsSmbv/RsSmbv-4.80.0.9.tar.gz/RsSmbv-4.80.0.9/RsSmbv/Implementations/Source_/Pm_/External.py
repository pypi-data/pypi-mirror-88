from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class External:
	"""External commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("external", core, parent)

	def get_deviation(self) -> float:
		"""[SOURce<HW>]:PM:EXTernal:DEViation \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PM:EXTernal:DEViation?')
		return Conversions.str_to_float(response)

	def set_deviation(self, deviation: float) -> None:
		"""[SOURce<HW>]:PM:EXTernal:DEViation \n
		No command help available \n
			:param deviation: No help available
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:PM:EXTernal:DEViation {param}')
