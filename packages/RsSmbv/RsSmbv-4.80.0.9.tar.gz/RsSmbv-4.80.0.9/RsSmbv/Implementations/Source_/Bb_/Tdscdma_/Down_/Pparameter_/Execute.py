from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:PPARameter:EXECute \n
		Presets the channel table of cell 1 with the parameters defined by the PPARameter commands. Scrambling Code 0 is
		automatically selected. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:PPARameter:EXECute')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:PPARameter:EXECute \n
		Presets the channel table of cell 1 with the parameters defined by the PPARameter commands. Scrambling Code 0 is
		automatically selected. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:PPARameter:EXECute')
