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
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:POWer:OFFSet \n
		Sets the power offset of the active channels of the additional user equipment relative to the power of the active
		channels of the reference station UE4. The offset applies to all the additional user equipment. The resultant overall
		power must fall within the range 0 ... - 80 dB. If the value is above or below this range, it is limited automatically. \n
			:return: offset: float Range: -80 to 0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:POWer:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:POWer:OFFSet \n
		Sets the power offset of the active channels of the additional user equipment relative to the power of the active
		channels of the reference station UE4. The offset applies to all the additional user equipment. The resultant overall
		power must fall within the range 0 ... - 80 dB. If the value is above or below this range, it is limited automatically. \n
			:param offset: float Range: -80 to 0
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:POWer:OFFSet {param}')
