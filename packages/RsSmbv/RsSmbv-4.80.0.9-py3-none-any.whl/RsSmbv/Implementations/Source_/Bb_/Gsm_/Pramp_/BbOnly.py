from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbOnly:
	"""BbOnly commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bbOnly", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:GSM:PRAMp:BBONly:[STATe] \n
		Note: This command is available for instruments with RF output only. Selects power ramping in the baseband only or mixed
		power ramping in the baseband and the RF section. The 'ON' setting is mandatory if, with power ramping active, only the
		baseband signal is output (I/Q outputs) , or, in case of two-path instruments, if a baseband signal is applied to two RF
		paths (RF A and RF B) . Only then can a signal with a defined, predictable level be output. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:PRAMp:BBONly:STATe?')
		return Conversions.str_to_bool(response)
