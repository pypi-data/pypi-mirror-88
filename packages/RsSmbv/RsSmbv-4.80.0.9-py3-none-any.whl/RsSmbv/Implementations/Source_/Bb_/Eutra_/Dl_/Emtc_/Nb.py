from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nb:
	"""Nb commands group definition. 9 total commands, 0 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nb", core, parent)

	def get_hoffset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:HOFFset \n
		Sets the number of narrowbands between two consecutive MPDCCH or PDSCH hops. \n
			:return: hopping_offset: integer Range: 1 to 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:HOFFset?')
		return Conversions.str_to_int(response)

	def set_hoffset(self, hopping_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:HOFFset \n
		Sets the number of narrowbands between two consecutive MPDCCH or PDSCH hops. \n
			:param hopping_offset: integer Range: 1 to 16
		"""
		param = Conversions.decimal_value_to_str(hopping_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:HOFFset {param}')

	# noinspection PyTypeChecker
	def get_hopping(self) -> enums.NumbersD:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:HOPPing \n
		Sets the number of narrowbands over which MPDCCH or PDSCH hops. \n
			:return: num_nb_hopping: 2| 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:HOPPing?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersD)

	def set_hopping(self, num_nb_hopping: enums.NumbersD) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:HOPPing \n
		Sets the number of narrowbands over which MPDCCH or PDSCH hops. \n
			:param num_nb_hopping: 2| 4
		"""
		param = Conversions.enum_scalar_to_str(num_nb_hopping, enums.NumbersD)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:HOPPing {param}')

	# noinspection PyTypeChecker
	def get_ivla(self) -> enums.EutraIotHoppingIvl:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:IVLA \n
		Sets the number of consecutive subframes during which MPDCCH or PDSCH stays at the same narrowband before hopping to
		another narrowband. \n
			:return: hopping_ivl_a: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:IVLA?')
		return Conversions.str_to_scalar_enum(response, enums.EutraIotHoppingIvl)

	def set_ivla(self, hopping_ivl_a: enums.EutraIotHoppingIvl) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:IVLA \n
		Sets the number of consecutive subframes during which MPDCCH or PDSCH stays at the same narrowband before hopping to
		another narrowband. \n
			:param hopping_ivl_a: H1| H2| H4| H5| H8| H10| H16| H20| H40
		"""
		param = Conversions.enum_scalar_to_str(hopping_ivl_a, enums.EutraIotHoppingIvl)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:IVLA {param}')

	# noinspection PyTypeChecker
	def get_ivlb(self) -> enums.EutraIotHoppingIvl:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:IVLB \n
		Sets the number of consecutive subframes during which MPDCCH or PDSCH stays at the same narrowband before hopping to
		another narrowband. \n
			:return: hopping_ivl_b: H1| H2| H4| H5| H8| H10| H16| H20| H40
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:IVLB?')
		return Conversions.str_to_scalar_enum(response, enums.EutraIotHoppingIvl)

	def set_ivlb(self, hopping_ivl_b: enums.EutraIotHoppingIvl) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:IVLB \n
		Sets the number of consecutive subframes during which MPDCCH or PDSCH stays at the same narrowband before hopping to
		another narrowband. \n
			:param hopping_ivl_b: H1| H2| H4| H5| H8| H10| H16| H20| H40
		"""
		param = Conversions.enum_scalar_to_str(hopping_ivl_b, enums.EutraIotHoppingIvl)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:IVLB {param}')

	def get_nn_bands(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:NNBands \n
		No command help available \n
			:return: num_narrow_bands: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:NNBands?')
		return Conversions.str_to_int(response)

	def get_phopping(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:PHOPping \n
		Enables hopping for the random access. \n
			:return: paging_hopping: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:PHOPping?')
		return Conversions.str_to_bool(response)

	def set_phopping(self, paging_hopping: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:PHOPping \n
		Enables hopping for the random access. \n
			:param paging_hopping: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(paging_hopping)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:PHOPping {param}')

	def get_pstnb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:PSTNb \n
		Sets the first used narrowband, if hoping is enabeld. \n
			:return: paging_starting_n: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:PSTNb?')
		return Conversions.str_to_int(response)

	def set_pstnb(self, paging_starting_n: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:PSTNb \n
		Sets the first used narrowband, if hoping is enabeld. \n
			:param paging_starting_n: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(paging_starting_n)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:PSTNb {param}')

	def get_rhoppping(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:RHOPpping \n
		Enables hopping for the random access. \n
			:return: ra_hopping: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:RHOPpping?')
		return Conversions.str_to_bool(response)

	def set_rhoppping(self, ra_hopping: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:RHOPpping \n
		Enables hopping for the random access. \n
			:param ra_hopping: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(ra_hopping)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:RHOPpping {param}')

	def get_rstnb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:RSTNb \n
		Sets the first used narrowband, if hoping is enabeld. \n
			:return: ra_starting_nb: integer Range: 0 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:RSTNb?')
		return Conversions.str_to_int(response)

	def set_rstnb(self, ra_starting_nb: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NB:RSTNb \n
		Sets the first used narrowband, if hoping is enabeld. \n
			:param ra_starting_nb: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(ra_starting_nb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NB:RSTNb {param}')
