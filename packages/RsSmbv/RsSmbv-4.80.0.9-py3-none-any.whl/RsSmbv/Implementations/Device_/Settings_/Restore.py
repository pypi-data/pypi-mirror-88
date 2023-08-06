from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Restore:
	"""Restore commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("restore", core, parent)

	def set(self) -> None:
		"""DEVice:SETTings:RESTore \n
		No command help available \n
		"""
		self._core.io.write(f'DEVice:SETTings:RESTore')

	def set_with_opc(self) -> None:
		"""DEVice:SETTings:RESTore \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DEVice:SETTings:RESTore')
