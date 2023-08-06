from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pramp:
	"""Pramp commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pramp", core, parent)

	def get_bb_only(self) -> bool:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:BBONly \n
		Activates or deactivates power ramping for the baseband signals. \n
			:return: bb_only: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:PRAMp:BBONly?')
		return Conversions.str_to_bool(response)

	def get_fdelay(self) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:FDELay \n
		Sets the offset in the falling edge of the envelope at the end of a burst. A positive value delays the ramp and a
		negative value causes an advance. \n
			:return: fdelay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:PRAMp:FDELay?')
		return Conversions.str_to_int(response)

	def set_fdelay(self, fdelay: int) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:FDELay \n
		Sets the offset in the falling edge of the envelope at the end of a burst. A positive value delays the ramp and a
		negative value causes an advance. \n
			:param fdelay: integer Range: -4 to 4
		"""
		param = Conversions.decimal_value_to_str(fdelay)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:PRAMp:FDELay {param}')

	def get_rdelay(self) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:RDELay \n
		Sets the offset in the falling edge of the envelope at the end of a burst. A positive value delays the ramp and a
		negative value causes an advance. \n
			:return: rdrlay: integer Range: -4 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:PRAMp:RDELay?')
		return Conversions.str_to_int(response)

	def set_rdelay(self, rdrlay: int) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:RDELay \n
		Sets the offset in the falling edge of the envelope at the end of a burst. A positive value delays the ramp and a
		negative value causes an advance. \n
			:param rdrlay: integer Range: -4 to 4
		"""
		param = Conversions.decimal_value_to_str(rdrlay)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:PRAMp:RDELay {param}')

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.RampFunc:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:SHAPe \n
		Selects the form of the transmitted power, i.e. the shape of the rising and falling edges during power ramp control. \n
			:return: shape: LINear| COSine
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:PRAMp:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.RampFunc)

	def set_shape(self, shape: enums.RampFunc) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:SHAPe \n
		Selects the form of the transmitted power, i.e. the shape of the rising and falling edges during power ramp control. \n
			:param shape: LINear| COSine
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.RampFunc)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:PRAMp:SHAPe {param}')

	def get_time(self) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:TIME \n
		Sets the power ramping rise time and fall time for a burst. \n
			:return: time: integer Range: 0 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:PRAMp:TIME?')
		return Conversions.str_to_int(response)

	def set_time(self, time: int) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:PRAMp:TIME \n
		Sets the power ramping rise time and fall time for a burst. \n
			:param time: integer Range: 0 to 4
		"""
		param = Conversions.decimal_value_to_str(time)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:PRAMp:TIME {param}')
