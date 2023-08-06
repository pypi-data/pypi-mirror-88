from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:CORRection:DEXChange:EXECute \n
		Executes the import or export of the selected correction list, according to the previously set transfer direction with
		command method RsSmbv.Source.Correction.Dexchange.mode. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:EXECute')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:CORRection:DEXChange:EXECute \n
		Executes the import or export of the selected correction list, according to the previously set transfer direction with
		command method RsSmbv.Source.Correction.Dexchange.mode. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:DEXChange:EXECute')
