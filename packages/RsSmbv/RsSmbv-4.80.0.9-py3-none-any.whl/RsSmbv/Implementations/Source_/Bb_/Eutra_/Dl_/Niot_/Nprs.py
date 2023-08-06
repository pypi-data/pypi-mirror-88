from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nprs:
	"""Nprs commands group definition. 12 total commands, 1 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nprs", core, parent)

	def clone(self) -> 'Nprs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nprs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bmp(self):
		"""bmp commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmp'):
			from .Nprs_.Bmp import Bmp
			self._bmp = Bmp(self._core, self._base)
		return self._bmp

	# noinspection PyTypeChecker
	def get_conf(self) -> enums.EutraNbiotNprsConfigType:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:CONF \n
		Defines which type of NPRS is used. \n
			:return: nprs_para_cfg: PA_A| PA_B| PA_AB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:CONF?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotNprsConfigType)

	def set_conf(self, nprs_para_cfg: enums.EutraNbiotNprsConfigType) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:CONF \n
		Defines which type of NPRS is used. \n
			:param nprs_para_cfg: PA_A| PA_B| PA_AB
		"""
		param = Conversions.enum_scalar_to_str(nprs_para_cfg, enums.EutraNbiotNprsConfigType)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:CONF {param}')

	def get_id(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:ID \n
		Sets the NPRS-ID used for the generation of the NPRS. \n
			:return: nprs_id: Integer Range: 0 to 4095
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:ID?')
		return Conversions.str_to_int(response)

	def set_id(self, nprs_id: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:ID \n
		Sets the NPRS-ID used for the generation of the NPRS. \n
			:param nprs_id: Integer Range: 0 to 4095
		"""
		param = Conversions.decimal_value_to_str(nprs_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:ID {param}')

	# noinspection PyTypeChecker
	class MtiaStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nprs_Muting_Info_A: List[str]: No parameter help available
			- Bit_Count: int: integer Sets the length of the periodically repeating NPRS bit sequence in number of NPRS position occurrences. Allowed are the following values: 2, 4, 8 or 16 Range: 2 to 16"""
		__meta_args_list = [
			ArgStruct('Nprs_Muting_Info_A', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nprs_Muting_Info_A: List[str] = None
			self.Bit_Count: int = None

	def get_mtia(self) -> MtiaStruct:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:MTIA \n
		Sets the nprs-MutingInfoA/nprs-MutingInfoB parameter, required if muting is used for the NPRS part A (and Part B)
		configurations. \n
			:return: structure: for return value, see the help for MtiaStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:MTIA?', self.__class__.MtiaStruct())

	def set_mtia(self, value: MtiaStruct) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:MTIA \n
		Sets the nprs-MutingInfoA/nprs-MutingInfoB parameter, required if muting is used for the NPRS part A (and Part B)
		configurations. \n
			:param value: see the help for MtiaStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:MTIA', value)

	# noinspection PyTypeChecker
	class MtibStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nprs_Muting_Info_B: List[str]: numeric '1' indicates that the NPRS is transmitted in the corresponding occasion; a '0' indicates a muted NPRS.
			- Bit_Count: int: integer Sets the length of the periodically repeating NPRS bit sequence in number of NPRS position occurrences. Allowed are the following values: 2, 4, 8 or 16 Range: 2 to 16"""
		__meta_args_list = [
			ArgStruct('Nprs_Muting_Info_B', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nprs_Muting_Info_B: List[str] = None
			self.Bit_Count: int = None

	def get_mtib(self) -> MtibStruct:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:MTIB \n
		Sets the nprs-MutingInfoA/nprs-MutingInfoB parameter, required if muting is used for the NPRS part A (and Part B)
		configurations. \n
			:return: structure: for return value, see the help for MtibStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:MTIB?', self.__class__.MtibStruct())

	def set_mtib(self, value: MtibStruct) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:MTIB \n
		Sets the nprs-MutingInfoA/nprs-MutingInfoB parameter, required if muting is used for the NPRS part A (and Part B)
		configurations. \n
			:param value: see the help for MtibStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:MTIB', value)

	# noinspection PyTypeChecker
	def get_period(self) -> enums.EutraNbiotNprsConfigbPeriod:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:PERiod \n
		For NPRS Part B configuration, sets the NPRS occasion period TNPRS. \n
			:return: nprs_period: PD_160| PD_320| PD_640| PD_1280
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:PERiod?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotNprsConfigbPeriod)

	def set_period(self, nprs_period: enums.EutraNbiotNprsConfigbPeriod) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:PERiod \n
		For NPRS Part B configuration, sets the NPRS occasion period TNPRS. \n
			:param nprs_period: PD_160| PD_320| PD_640| PD_1280
		"""
		param = Conversions.enum_scalar_to_str(nprs_period, enums.EutraNbiotNprsConfigbPeriod)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:PERiod {param}')

	def get_pow(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:POW \n
		Sets the power of the narrowband positioning reference signal (NPRS) . \n
			:return: nprs_power: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:POW?')
		return Conversions.str_to_float(response)

	def set_pow(self, nprs_power: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:POW \n
		Sets the power of the narrowband positioning reference signal (NPRS) . \n
			:param nprs_power: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(nprs_power)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:POW {param}')

	def get_sein(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:SEIN \n
		Specifies the index of the physical ressource block (PRB) containing the NPRS. \n
			:return: nprs_seq_info: integer Range: 0 to 174
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:SEIN?')
		return Conversions.str_to_int(response)

	def set_sein(self, nprs_seq_info: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:SEIN \n
		Specifies the index of the physical ressource block (PRB) containing the NPRS. \n
			:param nprs_seq_info: integer Range: 0 to 174
		"""
		param = Conversions.decimal_value_to_str(nprs_seq_info)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:SEIN {param}')

	# noinspection PyTypeChecker
	def get_sfnm(self) -> enums.EutraNbiotNprsConfigbSfnumb:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:SFNM \n
		For NPRS Part B configuration, sets the number of consecutive DL subframes NNPRS within one NPRS positioning occasion. \n
			:return: nprs_sf_number: SFNM_10| SFNM_20| SFNM_40| SFNM_80| SFNM_160| SFNM_320| SFNM_640| SFNM_1280
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:SFNM?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotNprsConfigbSfnumb)

	def set_sfnm(self, nprs_sf_number: enums.EutraNbiotNprsConfigbSfnumb) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:SFNM \n
		For NPRS Part B configuration, sets the number of consecutive DL subframes NNPRS within one NPRS positioning occasion. \n
			:param nprs_sf_number: SFNM_10| SFNM_20| SFNM_40| SFNM_80| SFNM_160| SFNM_320| SFNM_640| SFNM_1280
		"""
		param = Conversions.enum_scalar_to_str(nprs_sf_number, enums.EutraNbiotNprsConfigbSfnumb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:SFNM {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:STATe \n
		Enables the NPRS transmission. \n
			:return: nprs_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, nprs_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:STATe \n
		Enables the NPRS transmission. \n
			:param nprs_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(nprs_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:STATe {param}')

	# noinspection PyTypeChecker
	def get_sts_frame(self) -> enums.EutraNbiotNprsConfigbStartsf:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:STSFrame \n
		For NPRS Part B configuration, sets the subframe offset ɑNPRS. \n
			:return: nprs_start_sf: STSF0_8| STSF1_8| STSF2_8| STSF3_8| STSF4_8| STSF5_8| STSF6_8| STSF7_8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:STSFrame?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotNprsConfigbStartsf)

	def set_sts_frame(self, nprs_start_sf: enums.EutraNbiotNprsConfigbStartsf) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:NPRS:STSFrame \n
		For NPRS Part B configuration, sets the subframe offset ɑNPRS. \n
			:param nprs_start_sf: STSF0_8| STSF1_8| STSF2_8| STSF3_8| STSF4_8| STSF5_8| STSF6_8| STSF7_8
		"""
		param = Conversions.enum_scalar_to_str(nprs_start_sf, enums.EutraNbiotNprsConfigbStartsf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:NPRS:STSFrame {param}')
