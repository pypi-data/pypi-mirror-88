from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Usensor:
	"""Usensor commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usensor", core, parent)

	def set(self, device_id: str, serial: int) -> None:
		"""SLISt:SCAN:USENsor \n
		Scans for R&S NRP power sensors connected over a USB interface. \n
			:param device_id: String or Integer Range: 0 to 999999
			:param serial: integer Range: 0 to 999999
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('device_id', device_id, DataType.String), ArgSingle('serial', serial, DataType.Integer))
		self._core.io.write(f'SLISt:SCAN:USENsor {param}'.rstrip())
