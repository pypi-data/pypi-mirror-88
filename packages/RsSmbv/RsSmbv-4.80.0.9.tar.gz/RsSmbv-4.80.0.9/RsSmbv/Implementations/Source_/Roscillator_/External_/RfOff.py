from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfOff:
	"""RfOff commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfOff", core, parent)

	def get_state(self) -> bool:
		"""[SOURce]:ROSCillator:EXTernal:RFOFf:[STATe] \n
		Determines that the RF output is turned off when the external reference signal is selected, but missing. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:EXTernal:RFOFf:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce]:ROSCillator:EXTernal:RFOFf:[STATe] \n
		Determines that the RF output is turned off when the external reference signal is selected, but missing. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:ROSCillator:EXTernal:RFOFf:STATe {param}')
