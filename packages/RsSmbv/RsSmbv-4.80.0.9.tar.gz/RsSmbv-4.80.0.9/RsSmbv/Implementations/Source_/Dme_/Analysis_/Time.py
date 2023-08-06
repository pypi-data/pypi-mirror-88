from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	def get_ok(self) -> bool:
		"""[SOURce<HW>]:DME:ANALysis:TIME:OK \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:TIME:OK?')
		return Conversions.str_to_bool(response)

	def set_ok(self, state: bool) -> None:
		"""[SOURce<HW>]:DME:ANALysis:TIME:OK \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:TIME:OK {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:DME:ANALysis:TIME:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:TIME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:DME:ANALysis:TIME:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:TIME:STATe {param}')
