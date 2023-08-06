from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RstFrame:
	"""RstFrame commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rstFrame", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:RSTFrame \n
		Resets all subframe settings of the selected link direction to the default values. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:RSTFrame')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:RSTFrame \n
		Resets all subframe settings of the selected link direction to the default values. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:RSTFrame')
