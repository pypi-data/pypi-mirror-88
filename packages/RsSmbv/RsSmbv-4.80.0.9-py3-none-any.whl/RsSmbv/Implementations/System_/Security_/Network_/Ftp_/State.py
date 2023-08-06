from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, sec_pass_word: str, ftp_state: bool) -> None:
		"""SYSTem:SECurity:NETWork:FTP:[STATe] \n
		No command help available \n
			:param sec_pass_word: No help available
			:param ftp_state: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('ftp_state', ftp_state, DataType.Boolean))
		self._core.io.write(f'SYSTem:SECurity:NETWork:FTP:STATe {param}'.rstrip())

	def get(self) -> bool:
		"""SYSTem:SECurity:NETWork:FTP:[STATe] \n
		No command help available \n
			:return: ftp_state: No help available"""
		response = self._core.io.query_str(f'SYSTem:SECurity:NETWork:FTP:STATe?')
		return Conversions.str_to_bool(response)
