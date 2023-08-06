from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, sec_pass_word: str, mmem_prot_state: bool) -> None:
		"""SYSTem:SECurity:VOLMode:[STATe] \n
		Activates volatile mode, so that no user data can be written to the internal memory permanently. To enable volatile mode,
		reboot the instrument. Otherwise the change has no effect. \n
			:param sec_pass_word: string Current security password The default password is 123456.
			:param mmem_prot_state: 0| 1| OFF| ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('mmem_prot_state', mmem_prot_state, DataType.Boolean))
		self._core.io.write(f'SYSTem:SECurity:VOLMode:STATe {param}'.rstrip())

	def get(self) -> bool:
		"""SYSTem:SECurity:VOLMode:[STATe] \n
		Activates volatile mode, so that no user data can be written to the internal memory permanently. To enable volatile mode,
		reboot the instrument. Otherwise the change has no effect. \n
			:return: mmem_prot_state: 0| 1| OFF| ON"""
		response = self._core.io.query_str(f'SYSTem:SECurity:VOLMode:STATe?')
		return Conversions.str_to_bool(response)
