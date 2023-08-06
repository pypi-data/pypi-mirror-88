from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsPy:
	"""IsPy commands group definition. 19 total commands, 0 Sub-groups, 19 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("isPy", core, parent)

	# noinspection PyTypeChecker
	def get_chbw(self) -> enums.EutraCaChannelBandwidth:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:CHBW \n
		Queries the channel bandwidth of the interfering signal. \n
			:return: chan_bandwidth: BW20_00| BW10_00| BW5_00| BW3_00| BW1_40| BW15_00
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:CHBW?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCaChannelBandwidth)

	def get_clid(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:CLID \n
		Sets the Cell ID for the interfering signal. \n
			:return: cell_id: integer Range: 0 to 503
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:CLID?')
		return Conversions.str_to_int(response)

	def set_clid(self, cell_id: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:CLID \n
		Sets the Cell ID for the interfering signal. \n
			:param cell_id: integer Range: 0 to 503
		"""
		param = Conversions.decimal_value_to_str(cell_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:CLID {param}')

	# noinspection PyTypeChecker
	def get_duplex(self) -> enums.EutraDuplexMode:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:DUPLex \n
		Selects whether TDD or FDD duplexing mode is used. \n
			:return: duplex: TDD| FDD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:DUPLex?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)

	def set_duplex(self, duplex: enums.EutraDuplexMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:DUPLex \n
		Selects whether TDD or FDD duplexing mode is used. \n
			:param duplex: TDD| FDD
		"""
		param = Conversions.enum_scalar_to_str(duplex, enums.EutraDuplexMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:DUPLex {param}')

	# noinspection PyTypeChecker
	def get_fr_shift(self) -> enums.EutraTcwfReqShift:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:FRSHift \n
		No command help available \n
			:return: frequency_shift: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:FRSHift?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwfReqShift)

	def set_fr_shift(self, frequency_shift: enums.EutraTcwfReqShift) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:FRSHift \n
		No command help available \n
			:param frequency_shift: No help available
		"""
		param = Conversions.enum_scalar_to_str(frequency_shift, enums.EutraTcwfReqShift)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:FRSHift {param}')

	# noinspection PyTypeChecker
	def get_if_type(self) -> enums.EutraTcwInterfType:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:IFTYpe \n
			INTRO_CMD_HELP: Selects the type of the interfering signal: \n
			- For Blocking tests, the interfering signal can be an in-band EUTRA/LTE signal (EUTra) or out-of-band CW signal (CW) .
			- For Receiver Intermodulation tests, the first interfering signal can be an EUTRA/LTE signal (EUTra) or narrowband EUTRA signal (NEUTra) . The second interfering signal is always a CW signal (CW) . \n
			:return: interferer_type: NEUTra| EUTra| CW| UTRA
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:IFTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwInterfType)

	def set_if_type(self, interferer_type: enums.EutraTcwInterfType) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:IFTYpe \n
			INTRO_CMD_HELP: Selects the type of the interfering signal: \n
			- For Blocking tests, the interfering signal can be an in-band EUTRA/LTE signal (EUTra) or out-of-band CW signal (CW) .
			- For Receiver Intermodulation tests, the first interfering signal can be an EUTRA/LTE signal (EUTra) or narrowband EUTRA signal (NEUTra) . The second interfering signal is always a CW signal (CW) . \n
			:param interferer_type: NEUTra| EUTra| CW| UTRA
		"""
		param = Conversions.enum_scalar_to_str(interferer_type, enums.EutraTcwInterfType)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:IFTYpe {param}')

	def get_nrblock(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:NRBLock \n
		Queries the number of RBs used by the LTE interfering signal. \n
			:return: num_res_block: integer Range: 3 to 25
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:NRBLock?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_nta_offset(self) -> enums.EutraTcwsIgAdvNtaOffs:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:NTAOffset \n
		Sets the parameter NTAoffset. \n
			:return: sig_adv_nta_offset: NTA624| NTA0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:NTAOffset?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwsIgAdvNtaOffs)

	def set_nta_offset(self, sig_adv_nta_offset: enums.EutraTcwsIgAdvNtaOffs) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:NTAOffset \n
		Sets the parameter NTAoffset. \n
			:param sig_adv_nta_offset: NTA624| NTA0
		"""
		param = Conversions.enum_scalar_to_str(sig_adv_nta_offset, enums.EutraTcwsIgAdvNtaOffs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:NTAOffset {param}')

	# noinspection PyTypeChecker
	def get_oc_edge(self) -> enums.EutraTcwoFfsChanEdge:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:OCEDge \n
		Defines the offset of the interfering signal center frequency relative to edge of the wanted channel bandwidth. \n
			:return: offs_channel_edge: OCE12_5| OCE7_5| OCE2_5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:OCEDge?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwoFfsChanEdge)

	def set_oc_edge(self, offs_channel_edge: enums.EutraTcwoFfsChanEdge) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:OCEDge \n
		Defines the offset of the interfering signal center frequency relative to edge of the wanted channel bandwidth. \n
			:param offs_channel_edge: OCE12_5| OCE7_5| OCE2_5
		"""
		param = Conversions.enum_scalar_to_str(offs_channel_edge, enums.EutraTcwoFfsChanEdge)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:OCEDge {param}')

	def get_ort_cover(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:ORTCover \n
		No command help available \n
			:return: ortho_cover: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:ORTCover?')
		return Conversions.str_to_int(response)

	def get_ovrb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:OVRB \n
		No command help available \n
			:return: offset_vrb: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:OVRB?')
		return Conversions.str_to_int(response)

	def get_plevel(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:PLEVel \n
		Queries the power level of the interfering signal. \n
			:return: power_level: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:PLEVel?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_pr_condition(self) -> enums.EutraTcwPropagCond:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:PRCOndition \n
		No command help available \n
			:return: propag_condition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:PRCOndition?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwPropagCond)

	def get_rbc_frequency(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:RBCFrequency \n
		No command help available \n
			:return: rblock_cent_freq: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:RBCFrequency?')
		return Conversions.str_to_int(response)

	def get_rf_frequency(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:RFFRequency \n
		Queries the center frequency of the interfering signal. \n
			:return: rf_frequency: integer Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:RFFRequency?')
		return Conversions.str_to_int(response)

	def set_rf_frequency(self, rf_frequency: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:RFFRequency \n
		Queries the center frequency of the interfering signal. \n
			:param rf_frequency: integer Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(rf_frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:RFFRequency {param}')

	def get_tdd_config(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TDDConfig \n
		For TDD mode, selects the UL/DL Configuration number. \n
			:return: tdd_config: integer Range: 0 to 6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:TDDConfig?')
		return Conversions.str_to_int(response)

	def set_tdd_config(self, tdd_config: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TDDConfig \n
		For TDD mode, selects the UL/DL Configuration number. \n
			:param tdd_config: integer Range: 0 to 6
		"""
		param = Conversions.decimal_value_to_str(tdd_config)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:TDDConfig {param}')

	# noinspection PyTypeChecker
	def get_tm_codes(self) -> enums.UtraTcwtMcodes:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TMCodes \n
		No command help available \n
			:return: test_model_1_codes: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:TMCodes?')
		return Conversions.str_to_scalar_enum(response, enums.UtraTcwtMcodes)

	def set_tm_codes(self, test_model_1_codes: enums.UtraTcwtMcodes) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TMCodes \n
		No command help available \n
			:param test_model_1_codes: No help available
		"""
		param = Conversions.enum_scalar_to_str(test_model_1_codes, enums.UtraTcwtMcodes)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:TMCodes {param}')

	# noinspection PyTypeChecker
	def get_tmodel(self) -> enums.TestModel:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TMODel \n
		Queries the test model. The interfering signal is generated according to E-TM1.1 test model. \n
			:return: test_model: TM1_1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:TMODel?')
		return Conversions.str_to_scalar_enum(response, enums.TestModel)

	# noinspection PyTypeChecker
	def get_trequire(self) -> enums.TestRequire:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TREQuire \n
		No command help available \n
			:return: test_require: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:TREQuire?')
		return Conversions.str_to_scalar_enum(response, enums.TestRequire)

	def set_trequire(self, test_require: enums.TestRequire) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:TREQuire \n
		No command help available \n
			:param test_require: No help available
		"""
		param = Conversions.enum_scalar_to_str(test_require, enums.TestRequire)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:TREQuire {param}')

	def get_ueid(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:UEID \n
		Sets the UE ID/n_RNTI for the interfering signal. \n
			:return: ue_id_nrnti: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS:UEID?')
		return Conversions.str_to_int(response)

	def set_ueid(self, ue_id_nrnti: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS:UEID \n
		Sets the UE ID/n_RNTI for the interfering signal. \n
			:param ue_id_nrnti: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ue_id_nrnti)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS:UEID {param}')
