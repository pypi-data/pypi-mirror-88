from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Iqswap:
	"""Iqswap commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqswap", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:C2K:IQSWap:[STATe] \n
		This command inverts the Q-part of the baseband signal if set to ON. The signal on the baseband outputs meets the
		cdma2000 standard. In order to generate an RF signal that conforms to the standard, the 'I/Q Swap' function in the 'I/Q
		Modulator' menu must be enabled ('On') (SOURce:IQ:SWAP ON) . \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:IQSWap:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:C2K:IQSWap:[STATe] \n
		This command inverts the Q-part of the baseband signal if set to ON. The signal on the baseband outputs meets the
		cdma2000 standard. In order to generate an RF signal that conforms to the standard, the 'I/Q Swap' function in the 'I/Q
		Modulator' menu must be enabled ('On') (SOURce:IQ:SWAP ON) . \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:IQSWap:STATe {param}')
