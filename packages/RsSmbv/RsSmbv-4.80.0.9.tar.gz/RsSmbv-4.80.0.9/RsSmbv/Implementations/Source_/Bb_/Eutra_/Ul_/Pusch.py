from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pusch", core, parent)

	# noinspection PyTypeChecker
	def get_fh_mode(self) -> enums.EutraUlFreqHopMode:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:FHMode \n
		Sets the frequency hopping mode for PUSCH. \n
			:return: freq_hopping_mode: INTRa| INTer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:FHMode?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUlFreqHopMode)

	def set_fh_mode(self, freq_hopping_mode: enums.EutraUlFreqHopMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:FHMode \n
		Sets the frequency hopping mode for PUSCH. \n
			:param freq_hopping_mode: INTRa| INTer
		"""
		param = Conversions.enum_scalar_to_str(freq_hopping_mode, enums.EutraUlFreqHopMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:FHMode {param}')

	def get_fh_offset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:FHOFfset \n
		Sets the PUSCH Hopping Offset NRBHO. The PUSCH Hopping Offset determines the first physical resource block and the
		maximum number of physical resource blocks available for PUSCH transmission if PUSCH frequency hopping is used. \n
			:return: fhopp_offset: integer Range: dynamic to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:FHOFfset?')
		return Conversions.str_to_int(response)

	def set_fh_offset(self, fhopp_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:FHOFfset \n
		Sets the PUSCH Hopping Offset NRBHO. The PUSCH Hopping Offset determines the first physical resource block and the
		maximum number of physical resource blocks available for PUSCH transmission if PUSCH frequency hopping is used. \n
			:param fhopp_offset: integer Range: dynamic to dynamic
		"""
		param = Conversions.decimal_value_to_str(fhopp_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:FHOFfset {param}')

	def get_nhoffset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:NHOFfset \n
		Sets the narrowband hopping offset. \n
			:return: nb_hopping_offset: integer Range: 1 to 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:NHOFfset?')
		return Conversions.str_to_int(response)

	def set_nhoffset(self, nb_hopping_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:NHOFfset \n
		Sets the narrowband hopping offset. \n
			:param nb_hopping_offset: integer Range: 1 to 16
		"""
		param = Conversions.decimal_value_to_str(nb_hopping_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:NHOFfset {param}')

	def get_nhopping(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:NHOPping \n
		Enables narrowband hopping. \n
			:return: nb_hopping: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:NHOPping?')
		return Conversions.str_to_bool(response)

	def set_nhopping(self, nb_hopping: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:NHOPping \n
		Enables narrowband hopping. \n
			:param nb_hopping: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(nb_hopping)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:NHOPping {param}')

	def get_nosm(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:NOSM \n
		Sets the number of sub-bands (Nsb) into that the total range of physical resource blocks available for PUSCH transmission
		is divided. The frequency hopping is performed at sub-band level. \n
			:return: sub_band_count: integer Range: 1 to 110
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:NOSM?')
		return Conversions.str_to_int(response)

	def set_nosm(self, sub_band_count: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUSCh:NOSM \n
		Sets the number of sub-bands (Nsb) into that the total range of physical resource blocks available for PUSCH transmission
		is divided. The frequency hopping is performed at sub-band level. \n
			:param sub_band_count: integer Range: 1 to 110
		"""
		param = Conversions.decimal_value_to_str(sub_band_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUSCh:NOSM {param}')
