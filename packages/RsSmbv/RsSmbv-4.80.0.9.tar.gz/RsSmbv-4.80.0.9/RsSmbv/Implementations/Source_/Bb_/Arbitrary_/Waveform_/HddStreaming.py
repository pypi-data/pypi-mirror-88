from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HddStreaming:
	"""HddStreaming commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hddStreaming", core, parent)

	def get_blevel(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:WAVeform:HDDStreaming:BLEVel \n
		No command help available \n
			:return: blrvel: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WAVeform:HDDStreaming:BLEVel?')
		return Conversions.str_to_int(response)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:ARBitrary:WAVeform:HDDStreaming:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WAVeform:HDDStreaming:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WAVeform:HDDStreaming:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WAVeform:HDDStreaming:STATe {param}')
