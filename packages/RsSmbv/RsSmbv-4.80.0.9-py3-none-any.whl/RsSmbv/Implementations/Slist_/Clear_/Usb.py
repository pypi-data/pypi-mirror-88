from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Usb:
	"""Usb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usb", core, parent)

	def set(self) -> None:
		"""SLISt:CLEar:USB \n
		Removes all R&S NRP power sensors connected over USB from the list. \n
		"""
		self._core.io.write(f'SLISt:CLEar:USB')

	def set_with_opc(self) -> None:
		"""SLISt:CLEar:USB \n
		Removes all R&S NRP power sensors connected over USB from the list. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SLISt:CLEar:USB')
