from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UaiSetting:
	"""UaiSetting commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uaiSetting", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:NFC:UAISetting \n
		Triggers the instrument to automatically adjust the related parameters of the analog I and Q outputs. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:UAISetting')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:NFC:UAISetting \n
		Triggers the instrument to automatically adjust the related parameters of the analog I and Q outputs. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:UAISetting')
