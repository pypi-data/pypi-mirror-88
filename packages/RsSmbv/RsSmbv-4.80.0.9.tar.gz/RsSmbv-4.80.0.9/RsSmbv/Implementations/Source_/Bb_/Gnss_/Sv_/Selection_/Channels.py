from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channels:
	"""Channels commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channels", core, parent)

	def get_max(self) -> int:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:CHANnels:MAX \n
		Queries the maximum number of GNSS channels. The number depends on the simulation capacity, see 'Channel Budget'. \n
			:return: max_numb_channels: integer Range: 6 to 612
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:SELection:CHANnels:MAX?')
		return Conversions.str_to_int(response)

	def set_max(self, max_numb_channels: int) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:CHANnels:MAX \n
		Queries the maximum number of GNSS channels. The number depends on the simulation capacity, see 'Channel Budget'. \n
			:param max_numb_channels: integer Range: 6 to 612
		"""
		param = Conversions.decimal_value_to_str(max_numb_channels)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:CHANnels:MAX {param}')
