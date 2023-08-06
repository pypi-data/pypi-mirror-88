from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 7 total commands, 0 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccoding", core, parent)

	def get_mib(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:MIB \n
		Enables transmission of MIB data. \n
			:return: mib_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:MIB?')
		return Conversions.str_to_bool(response)

	def set_mib(self, mib_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:MIB \n
		Enables transmission of MIB data. \n
			:param mib_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(mib_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:MIB {param}')

	def get_mspare(self) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:MSPare \n
		Sets the 11 spare bits in the NPBCH transmission. \n
			:return: mib_spare_bits: 11-bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:MSPare?')
		return Conversions.str_to_str_list(response)

	def set_mspare(self, mib_spare_bits: List[str]) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:MSPare \n
		Sets the 11 spare bits in the NPBCH transmission. \n
			:param mib_spare_bits: 11-bits
		"""
		param = Conversions.list_to_csv_str(mib_spare_bits)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:MSPare {param}')

	def get_ncid(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:NCID \n
		Queries the NCell ID. \n
			:return: ncell_id: integer Range: 0 to 503
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:NCID?')
		return Conversions.str_to_int(response)

	def get_rsib(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:RSIB \n
		Queries the number of repetitions of the NDPSCH that carries SIB1-NB. \n
			:return: repetition_sib_1: integer Range: 0 to 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:RSIB?')
		return Conversions.str_to_int(response)

	def get_sib(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:SIB \n
		Sets the parameter scheduling info SIB1. \n
			:return: scheduling_sib_1: integer Range: 0 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:SIB?')
		return Conversions.str_to_int(response)

	def set_sib(self, scheduling_sib_1: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:SIB \n
		Sets the parameter scheduling info SIB1. \n
			:param scheduling_sib_1: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(scheduling_sib_1)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:SIB {param}')

	def get_soffset(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:SOFFset \n
		Sets the start SFN value. \n
			:return: sfn_offset: float Range: 0 to 1020
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:SOFFset?')
		return Conversions.str_to_float(response)

	def set_soffset(self, sfn_offset: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:SOFFset \n
		Sets the start SFN value. \n
			:param sfn_offset: float Range: 0 to 1020
		"""
		param = Conversions.decimal_value_to_str(sfn_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:SOFFset {param}')

	def get_stfsib_1(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:CCODing:STFSib1 \n
		Queries the first frame in that the NPDSCH transmission carrying SIB1-NB is allocated. \n
			:return: sib_1_start_frame: integer Range: 0 to 11
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:CCODing:STFSib1?')
		return Conversions.str_to_int(response)
