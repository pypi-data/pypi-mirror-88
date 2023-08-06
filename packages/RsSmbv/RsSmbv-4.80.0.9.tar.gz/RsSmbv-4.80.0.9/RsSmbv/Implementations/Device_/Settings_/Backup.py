from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Backup:
	"""Backup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("backup", core, parent)

	def set(self) -> None:
		"""DEVice:SETTings:BACKup \n
		No command help available \n
		"""
		self._core.io.write(f'DEVice:SETTings:BACKup')

	def set_with_opc(self) -> None:
		"""DEVice:SETTings:BACKup \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DEVice:SETTings:BACKup')
