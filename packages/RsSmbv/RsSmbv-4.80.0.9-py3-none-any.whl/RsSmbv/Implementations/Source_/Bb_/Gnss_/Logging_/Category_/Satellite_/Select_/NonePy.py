from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NonePy:
	"""NonePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nonePy", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:SELect:NONE \n
		Enables or disables all of the available SV IDs. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:SELect:NONE')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:SELect:NONE \n
		Enables or disables all of the available SV IDs. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:SELect:NONE')
