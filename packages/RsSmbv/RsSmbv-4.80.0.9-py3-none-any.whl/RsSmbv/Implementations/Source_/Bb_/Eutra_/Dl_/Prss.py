from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prss:
	"""Prss commands group definition. 8 total commands, 1 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prss", core, parent)

	def clone(self) -> 'Prss':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Prss(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def tprs(self):
		"""tprs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tprs'):
			from .Prss_.Tprs import Tprs
			self._tprs = Tprs(self._core, self._base)
		return self._tprs

	# noinspection PyTypeChecker
	def get_bw(self) -> enums.EutraCaChannelBandwidth:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:BW \n
		Defines the bandwidth in which the PRS is transmitted. \n
			:return: prs_bandwidth: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:BW?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCaChannelBandwidth)

	def set_bw(self, prs_bandwidth: enums.EutraCaChannelBandwidth) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:BW \n
		Defines the bandwidth in which the PRS is transmitted. \n
			:param prs_bandwidth: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00
		"""
		param = Conversions.enum_scalar_to_str(prs_bandwidth, enums.EutraCaChannelBandwidth)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:BW {param}')

	def get_ci(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:CI \n
		Sets the PRS Configuration Index IPRS as defined in 3GPP TS 36.211, table 6.10.4.3-1. \n
			:return: conf_idx: integer Range: 0 to 2399
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:CI?')
		return Conversions.str_to_int(response)

	def set_ci(self, conf_idx: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:CI \n
		Sets the PRS Configuration Index IPRS as defined in 3GPP TS 36.211, table 6.10.4.3-1. \n
			:param conf_idx: integer Range: 0 to 2399
		"""
		param = Conversions.decimal_value_to_str(conf_idx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:CI {param}')

	def get_dprs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:DPRS \n
		Queries the subframe offset of the PRS generation (DeltaPRS) as defined in 3GPP TS 36.211, table 6.10.4.3-1. \n
			:return: delta_prs: integer Range: 0 to 1279
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:DPRS?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	class MiPatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Prs_Muting_Info: List[str]: numeric Each bit defines the PRS state of one PRS occasion 0 PRS is muted 1 PRS is transmitted
			- Bit_Count: int: integer 2, 4, 8 or 16 bits Range: 2 to 16"""
		__meta_args_list = [
			ArgStruct('Prs_Muting_Info', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Prs_Muting_Info: List[str] = None
			self.Bit_Count: int = None

	def get_mi_pattern(self) -> MiPatternStruct:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:MIPattern \n
		Specifies a bit pattern that defines the muted and not muted PRS. \n
			:return: structure: for return value, see the help for MiPatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:MIPattern?', self.__class__.MiPatternStruct())

	def set_mi_pattern(self, value: MiPatternStruct) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:MIPattern \n
		Specifies a bit pattern that defines the muted and not muted PRS. \n
			:param value: see the help for MiPatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:MIPattern', value)

	# noinspection PyTypeChecker
	def get_nprs(self) -> enums.EutraNprs:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:NPRS \n
		Defines the number of consecutive DL subframes in that PRS are transmitted. \n
			:return: number_prs: 1| 2| 4| 6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:NPRS?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNprs)

	def set_nprs(self, number_prs: enums.EutraNprs) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:NPRS \n
		Defines the number of consecutive DL subframes in that PRS are transmitted. \n
			:param number_prs: 1| 2| 4| 6
		"""
		param = Conversions.enum_scalar_to_str(number_prs, enums.EutraNprs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:NPRS {param}')

	def get_pow(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:POW \n
		Sets the power of a PRS resource element relative to the power of a common reference signal resource element. \n
			:return: prs_power: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:POW?')
		return Conversions.str_to_float(response)

	def set_pow(self, prs_power: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:POW \n
		Sets the power of a PRS resource element relative to the power of a common reference signal resource element. \n
			:param prs_power: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(prs_power)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:POW {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:STATe \n
		Enables the generation of the PRS. \n
			:return: prs_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PRSS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, prs_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:STATe \n
		Enables the generation of the PRS. \n
			:param prs_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(prs_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:STATe {param}')
