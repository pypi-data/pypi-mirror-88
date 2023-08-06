from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_offset(self) -> float:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:POWer:OFFSet \n
		The command sets the power offset of the active channels of the additional mobile stations relative to the power of the
		active channels of the reference station MS4. The offset applies to all the additional mobile stations. The resultant
		overall power must fall within the range 0 ... - 80 dB. If the value is above or below this range, it is limited
		automatically. \n
			:return: offset: float Range: -80 dB to 0 dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:POWer:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:POWer:OFFSet \n
		The command sets the power offset of the active channels of the additional mobile stations relative to the power of the
		active channels of the reference station MS4. The offset applies to all the additional mobile stations. The resultant
		overall power must fall within the range 0 ... - 80 dB. If the value is above or below this range, it is limited
		automatically. \n
			:param offset: float Range: -80 dB to 0 dB
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:POWer:OFFSet {param}')
