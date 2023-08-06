from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.Utilities import trim_str_response
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcch:
	"""Mcch commands group definition. 15 total commands, 3 Sub-groups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcch", core, parent)

	def clone(self) -> 'Mcch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mcch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aval(self):
		"""aval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aval'):
			from .Mcch_.Aval import Aval
			self._aval = Aval(self._core, self._base)
		return self._aval

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Mcch_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .Mcch_.TbSize import TbSize
			self._tbSize = TbSize(self._core, self._base)
		return self._tbSize

	# noinspection PyTypeChecker
	def get_data(self) -> enums.DataSour:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:DATA \n
		Sets the data source used for the MCCH. \n
			:return: data_source: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)

	def set_data(self, data_source: enums.DataSour) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:DATA \n
		Sets the data source used for the MCCH. \n
			:param data_source: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE
		"""
		param = Conversions.enum_scalar_to_str(data_source, enums.DataSour)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:DATA {param}')

	def get_dlist(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:DLISt \n
		Sets the data list used as data source for MCCH. \n
			:return: data_list: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:DLISt?')
		return trim_str_response(response)

	def set_dlist(self, data_list: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:DLISt \n
		Sets the data list used as data source for MCCH. \n
			:param data_list: string
		"""
		param = Conversions.value_to_quoted_str(data_list)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:DLISt {param}')

	# noinspection PyTypeChecker
	def get_mcs(self) -> enums.EutraMcchMcs:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:MCS \n
		Defines the Modulation and Coding Scheme (MCS) applicable for the subframes indicated by the 'MCCH Allocation value' and
		for the first subframe of each MCH scheduling period (which may contain the MCH scheduling information provided by MAC) . \n
			:return: mcs: MCS19| MCS13| MCS7| MCS2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:MCS?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMcchMcs)

	def set_mcs(self, mcs: enums.EutraMcchMcs) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:MCS \n
		Defines the Modulation and Coding Scheme (MCS) applicable for the subframes indicated by the 'MCCH Allocation value' and
		for the first subframe of each MCH scheduling period (which may contain the MCH scheduling information provided by MAC) . \n
			:param mcs: MCS19| MCS13| MCS7| MCS2
		"""
		param = Conversions.enum_scalar_to_str(mcs, enums.EutraMcchMcs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:MCS {param}')

	# noinspection PyTypeChecker
	def get_mper(self) -> enums.EutraMcchModPer:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:MPER \n
		Sets the MCCH Modification Period. \n
			:return: modif_period: MP512| MP1024
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:MPER?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMcchModPer)

	def set_mper(self, modif_period: enums.EutraMcchModPer) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:MPER \n
		Sets the MCCH Modification Period. \n
			:param modif_period: MP512| MP1024
		"""
		param = Conversions.enum_scalar_to_str(modif_period, enums.EutraMcchModPer)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:MPER {param}')

	def get_noffset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NOFFset \n
		Defines, together with the method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.Ai.Mcch.nrc, the radio frames in which the MCCH
		information change notification is scheduled. \n
			:return: notif_offset: integer Range: 0 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NOFFset?')
		return Conversions.str_to_int(response)

	def set_noffset(self, notif_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NOFFset \n
		Defines, together with the method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.Ai.Mcch.nrc, the radio frames in which the MCCH
		information change notification is scheduled. \n
			:param notif_offset: integer Range: 0 to 10
		"""
		param = Conversions.decimal_value_to_str(notif_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NOFFset {param}')

	# noinspection PyTypeChecker
	class NpatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Notif_Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Notif_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Notif_Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_npattern(self) -> NpatternStruct:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern \n
		Sets the pattern for the notification bits sent on PDCCH DCI format 1c. \n
			:return: structure: for return value, see the help for NpatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern?', self.__class__.NpatternStruct())

	def set_npattern(self, value: NpatternStruct) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern \n
		Sets the pattern for the notification bits sent on PDCCH DCI format 1c. \n
			:param value: see the help for NpatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NPATtern', value)

	# noinspection PyTypeChecker
	def get_nrc(self) -> enums.EutraMbsfnNotRepCoef:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NRC \n
		Selects the current change notification repetition period common for all MCCHs that are configured. \n
			:return: notif_repet_coeff: NRC2| NRC4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NRC?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMbsfnNotRepCoef)

	def set_nrc(self, notif_repet_coeff: enums.EutraMbsfnNotRepCoef) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NRC \n
		Selects the current change notification repetition period common for all MCCHs that are configured. \n
			:param notif_repet_coeff: NRC2| NRC4
		"""
		param = Conversions.enum_scalar_to_str(notif_repet_coeff, enums.EutraMbsfnNotRepCoef)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NRC {param}')

	def get_nsi(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NSI \n
		Defines the subframe used to transmit MCCH change notifications on PDCCH. \n
			:return: index: integer In FDD: values 1 to 6 correspond with subframes #1, #2, #3, #6, #7 and #8 In TDD: values 1 to 5 correspond with subframe #3, #4, #7, #8 and #9 Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NSI?')
		return Conversions.str_to_int(response)

	def set_nsi(self, index: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:NSI \n
		Defines the subframe used to transmit MCCH change notifications on PDCCH. \n
			:param index: integer In FDD: values 1 to 6 correspond with subframes #1, #2, #3, #6, #7 and #8 In TDD: values 1 to 5 correspond with subframe #3, #4, #7, #8 and #9 Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(index)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:NSI {param}')

	def get_offs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:OFFS \n
		Indicates, together with the method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.Ai.Mcch.rper, the radio frames in which MCCH is
		scheduled. \n
			:return: mcch_offset: integer Range: 0 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:OFFS?')
		return Conversions.str_to_int(response)

	def set_offs(self, mcch_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:OFFS \n
		Indicates, together with the method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.Ai.Mcch.rper, the radio frames in which MCCH is
		scheduled. \n
			:param mcch_offset: integer Range: 0 to 10
		"""
		param = Conversions.decimal_value_to_str(mcch_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:OFFS {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_pattern(self) -> PatternStruct:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:PATTern \n
		Sets the pattern used as data source for the MCCH. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:PATTern \n
		Sets the pattern used as data source for the MCCH. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:PATTern', value)

	# noinspection PyTypeChecker
	def get_rper(self) -> enums.EutraMcchRepPer:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:RPER \n
		Defines the interval between transmissions of MCCH information in radio frames. \n
			:return: repet_period: RP64| RP32| RP128| RP256
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:RPER?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMcchRepPer)

	def set_rper(self, repet_period: enums.EutraMcchRepPer) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:RPER \n
		Defines the interval between transmissions of MCCH information in radio frames. \n
			:param repet_period: RP64| RP32| RP128| RP256
		"""
		param = Conversions.enum_scalar_to_str(repet_period, enums.EutraMcchRepPer)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:RPER {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:STATe \n
		Enables/disables the MCCH. \n
			:return: mcch_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, mcch_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:STATe \n
		Enables/disables the MCCH. \n
			:param mcch_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(mcch_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:STATe {param}')
