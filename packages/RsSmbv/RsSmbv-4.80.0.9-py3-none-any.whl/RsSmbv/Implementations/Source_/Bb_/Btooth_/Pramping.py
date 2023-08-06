from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pramping:
	"""Pramping commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pramping", core, parent)

	def get_foffset(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:FOFFset \n
		Sets the offset of the falling edge of a burst. The offset is specified by the selected number of symbols.
		Negative values shift the falling edge to earlier positions, which results in a corresponding number of skipped symbols
		at the end of the burst. Positive values shift the falling edge to later positions, which results in a corresponding
		number of added 0 padding symbols following the burst. \n
			:return: fo_ffset: integer Range: -32 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PRAMping:FOFFset?')
		return Conversions.str_to_int(response)

	def set_foffset(self, fo_ffset: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:FOFFset \n
		Sets the offset of the falling edge of a burst. The offset is specified by the selected number of symbols.
		Negative values shift the falling edge to earlier positions, which results in a corresponding number of skipped symbols
		at the end of the burst. Positive values shift the falling edge to later positions, which results in a corresponding
		number of added 0 padding symbols following the burst. \n
			:param fo_ffset: integer Range: -32 to 32
		"""
		param = Conversions.decimal_value_to_str(fo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PRAMping:FOFFset {param}')

	# noinspection PyTypeChecker
	def get_rfunction(self) -> enums.RampFunc:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:RFUNction \n
		The command selects the form of the transmitted power, i.e. the shape of the rising and falling edges during power ramp
		control. \n
			:return: rfunction: LINear| COSine
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PRAMping:RFUNction?')
		return Conversions.str_to_scalar_enum(response, enums.RampFunc)

	def set_rfunction(self, rfunction: enums.RampFunc) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:RFUNction \n
		The command selects the form of the transmitted power, i.e. the shape of the rising and falling edges during power ramp
		control. \n
			:param rfunction: LINear| COSine
		"""
		param = Conversions.enum_scalar_to_str(rfunction, enums.RampFunc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PRAMping:RFUNction {param}')

	def get_roffset(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:ROFFset \n
		Sets the offset of the rising edge of a burst. The offset is specified by the selected number of symbols. Negative values
		shift the rising edge to earlier positions, which results in a corresponding number of added 0 padding symbols before the
		burst. Positive values shift the rising edge to later positions, which results in a corresponding number of skipped
		symbols at the beginning of the burst. \n
			:return: roffset: integer Range: -32 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PRAMping:ROFFset?')
		return Conversions.str_to_int(response)

	def set_roffset(self, roffset: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:ROFFset \n
		Sets the offset of the rising edge of a burst. The offset is specified by the selected number of symbols. Negative values
		shift the rising edge to earlier positions, which results in a corresponding number of added 0 padding symbols before the
		burst. Positive values shift the rising edge to later positions, which results in a corresponding number of skipped
		symbols at the beginning of the burst. \n
			:param roffset: integer Range: -32 to 32
		"""
		param = Conversions.decimal_value_to_str(roffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PRAMping:ROFFset {param}')

	def get_rtime(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:RTIMe \n
		Sets the ramp time, which extends the burst by a corresponding number of 0 padding symbols at the beginning and the end
		of a burst. During this period of time, power ramping is based on the specified ramp function. \n
			:return: rtime: integer Range: 1 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PRAMping:RTIMe?')
		return Conversions.str_to_int(response)

	def set_rtime(self, rtime: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PRAMping:RTIMe \n
		Sets the ramp time, which extends the burst by a corresponding number of 0 padding symbols at the beginning and the end
		of a burst. During this period of time, power ramping is based on the specified ramp function. \n
			:param rtime: integer Range: 1 to 32
		"""
		param = Conversions.decimal_value_to_str(rtime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PRAMping:RTIMe {param}')
