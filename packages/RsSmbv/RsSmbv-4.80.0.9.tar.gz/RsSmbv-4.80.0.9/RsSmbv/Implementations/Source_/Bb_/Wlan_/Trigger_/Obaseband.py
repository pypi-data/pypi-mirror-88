from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Obaseband:
	"""Obaseband commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("obaseband", core, parent)

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:OBASeband:DELay \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:OBASeband:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:OBASeband:DELay \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:OBASeband:DELay {param}')

	def get_inhibit(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:OBASeband:INHibit \n
		No command help available \n
			:return: inhibit: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:OBASeband:INHibit?')
		return Conversions.str_to_float(response)

	def set_inhibit(self, inhibit: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:OBASeband:INHibit \n
		No command help available \n
			:param inhibit: No help available
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:OBASeband:INHibit {param}')
