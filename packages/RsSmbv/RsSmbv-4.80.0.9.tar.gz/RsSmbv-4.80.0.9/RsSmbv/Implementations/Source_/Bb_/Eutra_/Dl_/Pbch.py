from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pbch:
	"""Pbch commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pbch", core, parent)

	def get_mib(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:MIB \n
		Enables transmission of real MIB data. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PBCH:MIB?')
		return Conversions.str_to_bool(response)

	def set_mib(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:MIB \n
		Enables transmission of real MIB data. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PBCH:MIB {param}')

	def get_mspare(self) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:MSPare \n
		Sets the 10 spare bits in the PBCH transmission. \n
			:return: mib_spare_bits: 64 bit
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PBCH:MSPare?')
		return Conversions.str_to_str_list(response)

	def set_mspare(self, mib_spare_bits: List[str]) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:MSPare \n
		Sets the 10 spare bits in the PBCH transmission. \n
			:param mib_spare_bits: 64 bit
		"""
		param = Conversions.list_to_csv_str(mib_spare_bits)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PBCH:MSPare {param}')

	def get_ratba(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:RATBa \n
		Sets the transmit energy ratio among the resource elements allocated for teh channel in the OFDM symbols containing
		reference signal (P_B) and such not containing one (P_A) . \n
			:return: ratio_pb_pa: float Range: -10 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PBCH:RATBa?')
		return Conversions.str_to_float(response)

	def set_ratba(self, ratio_pb_pa: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:RATBa \n
		Sets the transmit energy ratio among the resource elements allocated for teh channel in the OFDM symbols containing
		reference signal (P_B) and such not containing one (P_A) . \n
			:param ratio_pb_pa: float Range: -10 to 10
		"""
		param = Conversions.decimal_value_to_str(ratio_pb_pa)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PBCH:RATBa {param}')

	def get_soffset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:SOFFset \n
		Sets an offset for the start value of the SFN (System Frame Number) . \n
			:return: sfn_offset: integer Range: 0 to 1020
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PBCH:SOFFset?')
		return Conversions.str_to_int(response)

	def set_soffset(self, sfn_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PBCH:SOFFset \n
		Sets an offset for the start value of the SFN (System Frame Number) . \n
			:param sfn_offset: integer Range: 0 to 1020
		"""
		param = Conversions.decimal_value_to_str(sfn_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PBCH:SOFFset {param}')
