from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Temporary:
	"""Temporary commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("temporary", core, parent)

	def delete(self) -> None:
		"""SYSTem:FILes:TEMPorary:DELete \n
		Deletes the temporary files from the internal memory or, if installed, from the Non-Volatile Memory. \n
		"""
		self._core.io.write(f'SYSTem:FILes:TEMPorary:DELete')

	def delete_with_opc(self) -> None:
		"""SYSTem:FILes:TEMPorary:DELete \n
		Deletes the temporary files from the internal memory or, if installed, from the Non-Volatile Memory. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:FILes:TEMPorary:DELete')
