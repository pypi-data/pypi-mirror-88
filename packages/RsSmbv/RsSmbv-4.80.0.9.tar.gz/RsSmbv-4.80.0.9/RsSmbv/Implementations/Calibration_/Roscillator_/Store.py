from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Store:
	"""Store commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("store", core, parent)

	def set(self) -> None:
		"""CALibration:ROSCillator:STORe \n
		No command help available \n
		"""
		self._core.io.write(f'CALibration:ROSCillator:STORe')

	def set_with_opc(self) -> None:
		"""CALibration:ROSCillator:STORe \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALibration:ROSCillator:STORe')
