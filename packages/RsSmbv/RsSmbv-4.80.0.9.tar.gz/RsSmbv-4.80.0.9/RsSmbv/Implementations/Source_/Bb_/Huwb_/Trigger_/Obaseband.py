from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Obaseband:
	"""Obaseband commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("obaseband", core, parent)

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:DELay \n
		Specifies the trigger delay (expressed as number of samples) for triggering by the trigger signal from the other path
		(two-path instruments only) . \n
			:return: delay: float Range: 0 to 2147483647
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:DELay \n
		Specifies the trigger delay (expressed as number of samples) for triggering by the trigger signal from the other path
		(two-path instruments only) . \n
			:param delay: float Range: 0 to 2147483647
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:DELay {param}')

	def get_inhibit(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:INHibit \n
		For triggering via the other path, specifies the number of samples by which a restart is inhibited. \n
			:return: inhibit: integer Range: 0 to 67108863
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:INHibit \n
		For triggering via the other path, specifies the number of samples by which a restart is inhibited. \n
			:param inhibit: integer Range: 0 to 67108863
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:INHibit {param}')

	def get_rdelay(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:RDELay \n
		Queries the actual trigger delay (expressed in time units) of the trigger signal from the second path. \n
			:return: int_oth_rdelay_sec: float Range: 0 to 688
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:RDELay?')
		return Conversions.str_to_float(response)

	def get_tdelay(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:TDELay \n
		Specifies the trigger delay (expressed in time units) for triggering by the trigger signal from the other path. \n
			:return: int_oth_delay_sec: float Range: 0 to 688
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:TDELay?')
		return Conversions.str_to_float(response)

	def set_tdelay(self, int_oth_delay_sec: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:OBASeband:TDELay \n
		Specifies the trigger delay (expressed in time units) for triggering by the trigger signal from the other path. \n
			:param int_oth_delay_sec: float Range: 0 to 688
		"""
		param = Conversions.decimal_value_to_str(int_oth_delay_sec)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OBASeband:TDELay {param}')
