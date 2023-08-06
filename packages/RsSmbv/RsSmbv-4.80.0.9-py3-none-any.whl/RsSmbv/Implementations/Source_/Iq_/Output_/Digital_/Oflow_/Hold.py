from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hold:
	"""Hold commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hold", core, parent)

	def reset(self) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:OFLow:HOLD:RESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:OFLow:HOLD:RESet')

	def reset_with_opc(self) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:OFLow:HOLD:RESet \n
		No command help available \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce:IQ:OUTPut:DIGital:OFLow:HOLD:RESet')

	def get_state(self) -> bool:
		"""[SOURce]:IQ:OUTPut:DIGital:OFLow:HOLD:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce:IQ:OUTPut:DIGital:OFLow:HOLD:STATe?')
		return Conversions.str_to_bool(response)
