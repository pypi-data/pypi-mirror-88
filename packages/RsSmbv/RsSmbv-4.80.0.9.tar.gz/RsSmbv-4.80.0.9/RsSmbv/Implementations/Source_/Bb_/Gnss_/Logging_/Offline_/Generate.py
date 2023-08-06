from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generate:
	"""Generate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("generate", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:GENerate \n
		Logging files are created and saved. Files with the same name are overwritten. To stop the generation, send method RsSmbv.
		Source.Bb.Gnss.Logging.Offline.abort. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:GENerate')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:GENerate \n
		Logging files are created and saved. Files with the same name are overwritten. To stop the generation, send method RsSmbv.
		Source.Bb.Gnss.Logging.Offline.abort. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:GENerate')
