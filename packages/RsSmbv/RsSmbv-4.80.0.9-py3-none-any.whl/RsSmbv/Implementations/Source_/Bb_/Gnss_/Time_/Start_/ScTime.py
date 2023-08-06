from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScTime:
	"""ScTime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scTime", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:SCTime \n
		Applies date and time settings of the operating system to the simulation start time. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:SCTime')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:SCTime \n
		Applies date and time settings of the operating system to the simulation start time. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:SCTime')
