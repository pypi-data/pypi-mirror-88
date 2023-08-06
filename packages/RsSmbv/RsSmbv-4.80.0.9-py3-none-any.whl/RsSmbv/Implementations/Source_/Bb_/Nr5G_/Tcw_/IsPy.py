from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsPy:
	"""IsPy commands group definition. 17 total commands, 0 Sub-groups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("isPy", core, parent)

	# noinspection PyTypeChecker
	def get_band(self) -> enums.Band:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:BAND \n
		Set the frequency band (n1 to n86) for the interfering signal. \n
			:return: band: N1| N2| N3| N5| N7| N8| N12| N20| N25| N28| N34| N38| N39| N40| N41| N50| N51| N66| N70| N71| N74| N75| N76| N77| N78| N79| N80| N81| N82| N83| N84| N86
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:BAND?')
		return Conversions.str_to_scalar_enum(response, enums.Band)

	def set_band(self, band: enums.Band) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:BAND \n
		Set the frequency band (n1 to n86) for the interfering signal. \n
			:param band: N1| N2| N3| N5| N7| N8| N12| N20| N25| N28| N34| N38| N39| N40| N41| N50| N51| N66| N70| N71| N74| N75| N76| N77| N78| N79| N80| N81| N82| N83| N84| N86
		"""
		param = Conversions.enum_scalar_to_str(band, enums.Band)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:BAND {param}')

	# noinspection PyTypeChecker
	def get_chbw(self) -> enums.Nr5Gcbw:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:CHBW \n
		Queries the channel bandwidth of the interfering signal. \n
			:return: isch_bw: BW5| BW10| BW15| BW20| BW25| BW40| BW50| BW60| BW100| BW80| BW400| BW200| BW30| BW70| BW90
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:CHBW?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5Gcbw)

	def get_clid(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:CLID \n
		No command help available \n
			:return: is_cell_id: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:CLID?')
		return Conversions.str_to_int(response)

	def set_clid(self, is_cell_id: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:CLID \n
		No command help available \n
			:param is_cell_id: No help available
		"""
		param = Conversions.decimal_value_to_str(is_cell_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:CLID {param}')

	def get_distance(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:DISTance \n
		Sets the distance between the test object and test antenna injecting the interferer signal. \n
			:return: distance: integer Range: 1 to 300
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:DISTance?')
		return Conversions.str_to_int(response)

	def set_distance(self, distance: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:DISTance \n
		Sets the distance between the test object and test antenna injecting the interferer signal. \n
			:param distance: integer Range: 1 to 300
		"""
		param = Conversions.decimal_value_to_str(distance)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:DISTance {param}')

	# noinspection PyTypeChecker
	def get_duplex(self) -> enums.EutraDuplexMode:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:DUPLex \n
		The duplexing mechanism used for the interfering signal can be switched between FDD and TDD. \n
			:return: is_duplexing: FDD| TDD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:DUPLex?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)

	def set_duplex(self, is_duplexing: enums.EutraDuplexMode) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:DUPLex \n
		The duplexing mechanism used for the interfering signal can be switched between FDD and TDD. \n
			:param is_duplexing: FDD| TDD
		"""
		param = Conversions.enum_scalar_to_str(is_duplexing, enums.EutraDuplexMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:DUPLex {param}')

	# noinspection PyTypeChecker
	def get_fr_shift(self) -> enums.FreqShift:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:FRSHift \n
		No command help available \n
			:return: is_freq_shift: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:FRSHift?')
		return Conversions.str_to_scalar_enum(response, enums.FreqShift)

	def set_fr_shift(self, is_freq_shift: enums.FreqShift) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:FRSHift \n
		No command help available \n
			:param is_freq_shift: No help available
		"""
		param = Conversions.enum_scalar_to_str(is_freq_shift, enums.FreqShift)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:FRSHift {param}')

	# noinspection PyTypeChecker
	def get_if_type(self) -> enums.InterfererTypeNr:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:IFTYpe \n
		No command help available \n
			:return: interferer_type_1: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:IFTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.InterfererTypeNr)

	def set_if_type(self, interferer_type_1: enums.InterfererTypeNr) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:IFTYpe \n
		No command help available \n
			:param interferer_type_1: No help available
		"""
		param = Conversions.enum_scalar_to_str(interferer_type_1, enums.InterfererTypeNr)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:IFTYpe {param}')

	def get_nrblock(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:NRBLock \n
		No command help available \n
			:return: is_num_rb: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:NRBLock?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_ofn(self) -> enums.OffsetFactorN:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:OFN \n
		Set the offset factor for the interfering signal. \n
			:return: offset_factor_n: OFN_1| OFN_2| OFN_3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:OFN?')
		return Conversions.str_to_scalar_enum(response, enums.OffsetFactorN)

	def set_ofn(self, offset_factor_n: enums.OffsetFactorN) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:OFN \n
		Set the offset factor for the interfering signal. \n
			:param offset_factor_n: OFN_1| OFN_2| OFN_3
		"""
		param = Conversions.enum_scalar_to_str(offset_factor_n, enums.OffsetFactorN)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:OFN {param}')

	def get_plevel(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:PLEVel \n
		Queries the power level of the interfering signal. \n
			:return: is_pow_level: float Range: -145 to 20, Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:PLEVel?')
		return Conversions.str_to_float(response)

	def get_rbc_frequency(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:RBCFrequency \n
		No command help available \n
			:return: is_rb_center_freq: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:RBCFrequency?')
		return Conversions.str_to_int(response)

	def get_rb_offset(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:RBOFfset \n
		No command help available \n
			:return: is_rb_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:RBOFfset?')
		return Conversions.str_to_int(response)

	def set_rb_offset(self, is_rb_offset: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:RBOFfset \n
		No command help available \n
			:param is_rb_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(is_rb_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:RBOFfset {param}')

	def get_rf_frequency(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:RFFRequency \n
		Queries the center frequency of the interfering signal 1 and 2. \n
			:return: is_rf_freq: integer Range: 100e+03 to 6e+09, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:RFFRequency?')
		return Conversions.str_to_int(response)

	def set_rf_frequency(self, is_rf_freq: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:RFFRequency \n
		Queries the center frequency of the interfering signal 1 and 2. \n
			:param is_rf_freq: integer Range: 100e+03 to 6e+09, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(is_rf_freq)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:RFFRequency {param}')

	# noinspection PyTypeChecker
	def get_sc_spacing(self) -> enums.Numerology:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:SCSPacing \n
		No command help available \n
			:return: is_scs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.Numerology)

	# noinspection PyTypeChecker
	def get_tmodel(self) -> enums.TestModel:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:TMODel \n
		Shows the test model set for the test case. The NR-TMs for FR1 are defined in TS 38.141-1 section 4.9.2. \n
			:return: test_model: TM1_1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:TMODel?')
		return Conversions.str_to_scalar_enum(response, enums.TestModel)

	# noinspection PyTypeChecker
	def get_trequire(self) -> enums.TestRequire:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:TREQuire \n
		No command help available \n
			:return: is_test_require: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:TREQuire?')
		return Conversions.str_to_scalar_enum(response, enums.TestRequire)

	def set_trequire(self, is_test_require: enums.TestRequire) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:TREQuire \n
		No command help available \n
			:param is_test_require: No help available
		"""
		param = Conversions.enum_scalar_to_str(is_test_require, enums.TestRequire)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:TREQuire {param}')

	def get_ueid(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:UEID \n
		No command help available \n
			:return: isu_eid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS:UEID?')
		return Conversions.str_to_int(response)

	def set_ueid(self, isu_eid: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS:UEID \n
		No command help available \n
			:param isu_eid: No help available
		"""
		param = Conversions.decimal_value_to_str(isu_eid)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:IS:UEID {param}')
