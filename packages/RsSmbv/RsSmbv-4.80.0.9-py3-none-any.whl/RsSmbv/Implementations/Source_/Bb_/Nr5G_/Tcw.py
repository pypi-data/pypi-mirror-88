from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tcw:
	"""Tcw commands group definition. 69 total commands, 8 Sub-groups, 13 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tcw", core, parent)

	def clone(self) -> 'Tcw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tcw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ant(self):
		"""ant commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ant'):
			from .Tcw_.Ant import Ant
			self._ant = Ant(self._core, self._base)
		return self._ant

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Tcw_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def awgn(self):
		"""awgn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_awgn'):
			from .Tcw_.Awgn import Awgn
			self._awgn = Awgn(self._core, self._base)
		return self._awgn

	@property
	def fa(self):
		"""fa commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fa'):
			from .Tcw_.Fa import Fa
			self._fa = Fa(self._core, self._base)
		return self._fa

	@property
	def is2(self):
		"""is2 commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_is2'):
			from .Tcw_.Is2 import Is2
			self._is2 = Is2(self._core, self._base)
		return self._is2

	@property
	def isPy(self):
		"""isPy commands group. 0 Sub-classes, 17 commands."""
		if not hasattr(self, '_isPy'):
			from .Tcw_.IsPy import IsPy
			self._isPy = IsPy(self._core, self._base)
		return self._isPy

	@property
	def rtf(self):
		"""rtf commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_rtf'):
			from .Tcw_.Rtf import Rtf
			self._rtf = Rtf(self._core, self._base)
		return self._rtf

	@property
	def ws(self):
		"""ws commands group. 5 Sub-classes, 17 commands."""
		if not hasattr(self, '_ws'):
			from .Tcw_.Ws import Ws
			self._ws = Ws(self._core, self._base)
		return self._ws

	def get_bewphi(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:TCW:BEWPhi \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the φ-axis (BeWθ,REFSENS) , applicable for FR1 only. \n
			:return: be_wphi_ref_sens: float Range: 0.1 to 360
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BEWPhi?')
		return Conversions.str_to_float(response)

	def set_bewphi(self, be_wphi_ref_sens: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:BEWPhi \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the φ-axis (BeWθ,REFSENS) , applicable for FR1 only. \n
			:param be_wphi_ref_sens: float Range: 0.1 to 360
		"""
		param = Conversions.decimal_value_to_str(be_wphi_ref_sens)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BEWPhi {param}')

	def get_bewthet(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:TCW:BEWThet \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the θ-axis (BeWθ,REFSENS) , applicable for FR1 only. \n
			:return: be_wthet_ref_sens: float Range: 0.1 to 360
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BEWThet?')
		return Conversions.str_to_float(response)

	def set_bewthet(self, be_wthet_ref_sens: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:BEWThet \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the θ-axis (BeWθ,REFSENS) , applicable for FR1 only. \n
			:param be_wthet_ref_sens: float Range: 0.1 to 360
		"""
		param = Conversions.decimal_value_to_str(be_wthet_ref_sens)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BEWThet {param}')

	# noinspection PyTypeChecker
	def get_bs_class(self) -> enums.BsClass:
		"""[SOURce<HW>]:BB:NR5G:TCW:BSCLass \n
		Sets the NR base station class. \n
			:return: bs_class: WIDE| MED| LOC
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BSCLass?')
		return Conversions.str_to_scalar_enum(response, enums.BsClass)

	def set_bs_class(self, bs_class: enums.BsClass) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:BSCLass \n
		Sets the NR base station class. \n
			:param bs_class: WIDE| MED| LOC
		"""
		param = Conversions.enum_scalar_to_str(bs_class, enums.BsClass)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BSCLass {param}')

	# noinspection PyTypeChecker
	def get_bs_type(self) -> enums.BsType:
		"""[SOURce<HW>]:BB:NR5G:TCW:BSTYpe \n
		Sets the base station type for the OTA settings as specified in D.5. \n
			:return: bs_type: BT1H| BT1O| BT2O BT1 Sets the BS type 1-H (FR1, hybrid) for the OTA settings. BT1O Sets the BS type 1-O (FR1) for the OTA settings. BT2O Sets the BS type 2-O (FR2) for the OTA settings.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BSTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BsType)

	def set_bs_type(self, bs_type: enums.BsType) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:BSTYpe \n
		Sets the base station type for the OTA settings as specified in D.5. \n
			:param bs_type: BT1H| BT1O| BT2O BT1 Sets the BS type 1-H (FR1, hybrid) for the OTA settings. BT1O Sets the BS type 1-O (FR1) for the OTA settings. BT2O Sets the BS type 2-O (FR2) for the OTA settings.
		"""
		param = Conversions.enum_scalar_to_str(bs_type, enums.BsType)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BSTYpe {param}')

	# noinspection PyTypeChecker
	def get_dcl_direction(self) -> enums.DeclaredDir:
		"""[SOURce<HW>]:BB:NR5G:TCW:DCLDirection \n
		Sets the reference for the OSDD. \n
			:return: declared_dir: OTHD| MREFD| OREFD OTHD Sets a value different than the minSENS and REFSENS as the reference for the OSDD. MREFD Sets the OTA minimum sensitivity (minSENS) value as the reference for the OSDD. OREFD Sets the OTA reference sensitivity (REFSENS) value as the reference for the OSDD.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:DCLDirection?')
		return Conversions.str_to_scalar_enum(response, enums.DeclaredDir)

	def set_dcl_direction(self, declared_dir: enums.DeclaredDir) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:DCLDirection \n
		Sets the reference for the OSDD. \n
			:param declared_dir: OTHD| MREFD| OREFD OTHD Sets a value different than the minSENS and REFSENS as the reference for the OSDD. MREFD Sets the OTA minimum sensitivity (minSENS) value as the reference for the OSDD. OREFD Sets the OTA reference sensitivity (REFSENS) value as the reference for the OSDD.
		"""
		param = Conversions.enum_scalar_to_str(declared_dir, enums.DeclaredDir)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:DCLDirection {param}')

	def get_e_50(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:TCW:E50 \n
		Sets the EISREFSENS_50M level value applicable in the OTA REFSENS RoAoA as specified in D.28. The EISREFSENS_50M value is
		the declared OTA reference sensitivity basis level for FR2 based on a reference measurement channel with 50MHz BS channel
		bandwidth. \n
			:return: eis_50_m: float Range: -119 to -86
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:E50?')
		return Conversions.str_to_float(response)

	def set_e_50(self, eis_50_m: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:E50 \n
		Sets the EISREFSENS_50M level value applicable in the OTA REFSENS RoAoA as specified in D.28. The EISREFSENS_50M value is
		the declared OTA reference sensitivity basis level for FR2 based on a reference measurement channel with 50MHz BS channel
		bandwidth. \n
			:param eis_50_m: float Range: -119 to -86
		"""
		param = Conversions.decimal_value_to_str(eis_50_m)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:E50 {param}')

	# noinspection PyTypeChecker
	def get_fr(self) -> enums.FreqRange:
		"""[SOURce<HW>]:BB:NR5G:TCW:FR \n
		No command help available \n
			:return: freq_range: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:FR?')
		return Conversions.str_to_scalar_enum(response, enums.FreqRange)

	def set_fr(self, freq_range: enums.FreqRange) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:FR \n
		No command help available \n
			:param freq_range: No help available
		"""
		param = Conversions.enum_scalar_to_str(freq_range, enums.FreqRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:FR {param}')

	# noinspection PyTypeChecker
	def get_marker_config(self) -> enums.MarkConf:
		"""[SOURce<HW>]:BB:NR5G:TCW:MARKerconfig \n
		Selects the marker configuration. The marker can be used to synchronize the measuring equipment to the signal generator. \n
			:return: marker_config: FRAM| UNCH FRAM The marker settings are customized for the selected test case. 'Radio Frame Start' markers are output; the marker delays are set equal to zero. UNCH The current marker settings of the signal generator are retained unchanged.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:MARKerconfig?')
		return Conversions.str_to_scalar_enum(response, enums.MarkConf)

	def set_marker_config(self, marker_config: enums.MarkConf) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:MARKerconfig \n
		Selects the marker configuration. The marker can be used to synchronize the measuring equipment to the signal generator. \n
			:param marker_config: FRAM| UNCH FRAM The marker settings are customized for the selected test case. 'Radio Frame Start' markers are output; the marker delays are set equal to zero. UNCH The current marker settings of the signal generator are retained unchanged.
		"""
		param = Conversions.enum_scalar_to_str(marker_config, enums.MarkConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:MARKerconfig {param}')

	def get_meis(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:TCW:MEIS \n
		Sets the lowest equivalent isotropic sensitivity value (EISminSENS) for the OSDD as specified in D.27. \n
			:return: minimum_eis: float Range: -145 to -10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:MEIS?')
		return Conversions.str_to_float(response)

	def set_meis(self, minimum_eis: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:MEIS \n
		Sets the lowest equivalent isotropic sensitivity value (EISminSENS) for the OSDD as specified in D.27. \n
			:param minimum_eis: float Range: -145 to -10
		"""
		param = Conversions.decimal_value_to_str(minimum_eis)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:MEIS {param}')

	# noinspection PyTypeChecker
	def get_release(self) -> enums.Release:
		"""[SOURce<HW>]:BB:NR5G:TCW:RELease \n
		Sets the 3GPP test specification used as a guideline for the test cases. \n
			:return: release: REL15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:RELease?')
		return Conversions.str_to_scalar_enum(response, enums.Release)

	def set_release(self, release: enums.Release) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:RELease \n
		Sets the 3GPP test specification used as a guideline for the test cases. \n
			:param release: REL15
		"""
		param = Conversions.enum_scalar_to_str(release, enums.Release)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:RELease {param}')

	# noinspection PyTypeChecker
	def get_spec(self) -> enums.TestSpec:
		"""[SOURce<HW>]:BB:NR5G:TCW:SPEC \n
		Specifies the 3GPP test specification. \n
			:return: test_spec: TS381411
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:SPEC?')
		return Conversions.str_to_scalar_enum(response, enums.TestSpec)

	def set_spec(self, test_spec: enums.TestSpec) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:SPEC \n
		Specifies the 3GPP test specification. \n
			:param test_spec: TS381411
		"""
		param = Conversions.enum_scalar_to_str(test_spec, enums.TestSpec)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:SPEC {param}')

	# noinspection PyTypeChecker
	def get_tc(self) -> enums.TestCase:
		"""[SOURce<HW>]:BB:NR5G:TCW:TC \n
		Selects the test case. \n
			:return: test_case: TS381411_TC72| TS381411_TC73| TS381411_TC741| TS381411_TC742A| TS381411_TC742B| TS381411_TC75| TS381411_TC77| TS381411_TC78| TS381411_TC821| TS381411_TC822| TS381411_TC823| TS381411_TC831| TS381411_TC8321| TS381411_TC8322| TS381411_TC8331| TS381411_TC8332| TS381411_TC834| TS381411_TC835| TS381411_TC8361A| TS381411_TC8361B| TS381411_TC841| TS381411_TC67| TS381412_TC72| TS381412_TC73| TS381412_TC74| TS381412_TC751| TS381412_TC752A| TS381412_TC752B| TS381412_TC76| TS381412_TC78| TS381412_TC79| TS381412_TC821| TS381412_TC822| TS381412_TC823| TS381412_TC831| TS381412_TC8321| TS381412_TC8322| TS381412_TC8331| TS381412_TC8332| TS381412_TC834| TS381412_TC835| TS381412_TC8361A| TS381412_TC8361B| TS381412_TC841| TS381412_TC68 The first part of the parameter indicates the specification and the second part the chapter in which the test case is defined. For example, TS381411_TC72 defines the test case specified in chapter 7.2. TS381411_TC72 chapter 7.2 Reference Sensitivity Level TS381411_TC73 chapter 7.3 Dynamic Range TS381411_TC741 chapter 7.4.1 Adjacent Channel Selectivity (ACS) TS381411_TC742A| chapter 7.4.2A In-band General Blocking TS381411_TC742B chapter 7.4.2B In-band Narrowband Blocking TS381411_TC75 chapter 7.5 Out-of-band Blocking TS381411_TC77 chapter 7.7 Receiver Intermodulation TS381411_TC78 chapter 7.8 In-channel Selectivity TS381411_TC821 chapter 8.2.1 PUSCH transform precoding disabled TS381411_TC822 chapter 8.2.2 PUSCH transform precoding enabled TS381411_TC823 chapter 8.2.3 UCI multiplexed on PUSCH TS381411_TC831 chapter 8.3.1 Performance requirements for PUCCH format 0 TS381411_TC8321 chapter 8.3.2.1 NACK to ACK detection for PUCCH format 1 TS381411_TC8322 chapter 8.3.2.2 ACK missed detection for PUCCH format 1 TS381411_TC8331 chapter 8.3.3.1 ACK missed detection for PUCCH format 2 TS381411_TC8332 chapter 8.3.3.2 UCI BLER for PUCCH format 2 TS381411_TC834 chapter 8.3.4 Performance requirements for PUCCH format 3 TS381411_TC835 chapter 8.3.5 Performance requirements for PUCCH format 4 TS381411_TC8361A chapter 8.3.6.1A NACK to ACK detection for multi-slot PUCCH format 1 TS381411_TC8361B chapter 8.3.6.1B ACK missed detection for multi-slot PUCCH format 1 TS381411_TC841 chapter 8.4.1 PRACH false alarm probability and missed detection TS381411_TC67 chapter 6.7 Reference sensitivity level TS381412_TC72 chapter 7.2 OTA sensitivity TS381412_TC73 chapter 7.3 OTA reference sensitivity level TS381412_TC74 chapter 7.4 OTA dynamic range TS381412_TC751 chapter 7.5.1 OTA adjacent channel selectivity (ACS) TS381412_TC752A chapter 7.5.2A OTA in-band general blocking TS381412_TC752B chapter 7.5.2B OTA in-band narrowband blocking TS381412_TC76 chapter 7.6 OTA out-of-band blocking TS381412_TC78 chapter 7.8 OTA receiver intermodulation TS381412_TC79 chapter 7.9 OTA in-channel selectivity TS381412_TC821 chapter 8.2.1 OTA PUSCH with transform precoding disabled TS381412_TC822 chapter 8.2.2 OTA PUSCH with transform precoding enabled TS381412_TC823 chapter 8.2.3 OTA UCI multiplexed on PUSCH TS381412_TC831 chapter 8.3.1 OTA performance requirements for PUCCH format 0 TS381412_TC8321 chapter 8.3.2.1 OTA NACK to ACK detection for PUCCH format 1 TS381412_TC8322 chapter 8.3.2.2 OTA ACK missed detection for PUCCH format 1 TS381412_TC8331 chapter 8.3.3.1 OTA ACK missed detection for PUCCH format 2 TS381412_TC8332 chapter 8.3.3.2 OTA UCI BLER for PUCCH format 2 TS381412_TC834 chapter 8.3.4 OTA performance requirements for PUCCH format 3 TS381412_TC835 chapter 8.3.5 OTA performance requirements for PUCCH format 4 TS381412_TC8361A chapter 8.3.6.1A OTA NACK to ACK detection for multi-slot PUCCH format 1 TS381412_TC8361B chapter 8.3.6.1B OTA ACK missed detection for multi-slot PUCCH format 1 TS381412_TC841 chapter 8.4.1 OTA PRACH false alarm probability and missed detection TS381412_TC68 chapter 6.8 OTA transmitter intermodulation
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:TC?')
		return Conversions.str_to_scalar_enum(response, enums.TestCase)

	def set_tc(self, test_case: enums.TestCase) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:TC \n
		Selects the test case. \n
			:param test_case: TS381411_TC72| TS381411_TC73| TS381411_TC741| TS381411_TC742A| TS381411_TC742B| TS381411_TC75| TS381411_TC77| TS381411_TC78| TS381411_TC821| TS381411_TC822| TS381411_TC823| TS381411_TC831| TS381411_TC8321| TS381411_TC8322| TS381411_TC8331| TS381411_TC8332| TS381411_TC834| TS381411_TC835| TS381411_TC8361A| TS381411_TC8361B| TS381411_TC841| TS381411_TC67| TS381412_TC72| TS381412_TC73| TS381412_TC74| TS381412_TC751| TS381412_TC752A| TS381412_TC752B| TS381412_TC76| TS381412_TC78| TS381412_TC79| TS381412_TC821| TS381412_TC822| TS381412_TC823| TS381412_TC831| TS381412_TC8321| TS381412_TC8322| TS381412_TC8331| TS381412_TC8332| TS381412_TC834| TS381412_TC835| TS381412_TC8361A| TS381412_TC8361B| TS381412_TC841| TS381412_TC68 The first part of the parameter indicates the specification and the second part the chapter in which the test case is defined. For example, TS381411_TC72 defines the test case specified in chapter 7.2. TS381411_TC72 chapter 7.2 Reference Sensitivity Level TS381411_TC73 chapter 7.3 Dynamic Range TS381411_TC741 chapter 7.4.1 Adjacent Channel Selectivity (ACS) TS381411_TC742A| chapter 7.4.2A In-band General Blocking TS381411_TC742B chapter 7.4.2B In-band Narrowband Blocking TS381411_TC75 chapter 7.5 Out-of-band Blocking TS381411_TC77 chapter 7.7 Receiver Intermodulation TS381411_TC78 chapter 7.8 In-channel Selectivity TS381411_TC821 chapter 8.2.1 PUSCH transform precoding disabled TS381411_TC822 chapter 8.2.2 PUSCH transform precoding enabled TS381411_TC823 chapter 8.2.3 UCI multiplexed on PUSCH TS381411_TC831 chapter 8.3.1 Performance requirements for PUCCH format 0 TS381411_TC8321 chapter 8.3.2.1 NACK to ACK detection for PUCCH format 1 TS381411_TC8322 chapter 8.3.2.2 ACK missed detection for PUCCH format 1 TS381411_TC8331 chapter 8.3.3.1 ACK missed detection for PUCCH format 2 TS381411_TC8332 chapter 8.3.3.2 UCI BLER for PUCCH format 2 TS381411_TC834 chapter 8.3.4 Performance requirements for PUCCH format 3 TS381411_TC835 chapter 8.3.5 Performance requirements for PUCCH format 4 TS381411_TC8361A chapter 8.3.6.1A NACK to ACK detection for multi-slot PUCCH format 1 TS381411_TC8361B chapter 8.3.6.1B ACK missed detection for multi-slot PUCCH format 1 TS381411_TC841 chapter 8.4.1 PRACH false alarm probability and missed detection TS381411_TC67 chapter 6.7 Reference sensitivity level TS381412_TC72 chapter 7.2 OTA sensitivity TS381412_TC73 chapter 7.3 OTA reference sensitivity level TS381412_TC74 chapter 7.4 OTA dynamic range TS381412_TC751 chapter 7.5.1 OTA adjacent channel selectivity (ACS) TS381412_TC752A chapter 7.5.2A OTA in-band general blocking TS381412_TC752B chapter 7.5.2B OTA in-band narrowband blocking TS381412_TC76 chapter 7.6 OTA out-of-band blocking TS381412_TC78 chapter 7.8 OTA receiver intermodulation TS381412_TC79 chapter 7.9 OTA in-channel selectivity TS381412_TC821 chapter 8.2.1 OTA PUSCH with transform precoding disabled TS381412_TC822 chapter 8.2.2 OTA PUSCH with transform precoding enabled TS381412_TC823 chapter 8.2.3 OTA UCI multiplexed on PUSCH TS381412_TC831 chapter 8.3.1 OTA performance requirements for PUCCH format 0 TS381412_TC8321 chapter 8.3.2.1 OTA NACK to ACK detection for PUCCH format 1 TS381412_TC8322 chapter 8.3.2.2 OTA ACK missed detection for PUCCH format 1 TS381412_TC8331 chapter 8.3.3.1 OTA ACK missed detection for PUCCH format 2 TS381412_TC8332 chapter 8.3.3.2 OTA UCI BLER for PUCCH format 2 TS381412_TC834 chapter 8.3.4 OTA performance requirements for PUCCH format 3 TS381412_TC835 chapter 8.3.5 OTA performance requirements for PUCCH format 4 TS381412_TC8361A chapter 8.3.6.1A OTA NACK to ACK detection for multi-slot PUCCH format 1 TS381412_TC8361B chapter 8.3.6.1B OTA ACK missed detection for multi-slot PUCCH format 1 TS381412_TC841 chapter 8.4.1 OTA PRACH false alarm probability and missed detection TS381412_TC68 chapter 6.8 OTA transmitter intermodulation
		"""
		param = Conversions.enum_scalar_to_str(test_case, enums.TestCase)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:TC {param}')

	# noinspection PyTypeChecker
	def get_trigger_config(self) -> enums.TrigConf:
		"""[SOURce<HW>]:BB:NR5G:TCW:TRIGgerconfig \n
		Selects the trigger configuration. The trigger is used to synchronize the signal generator to the other equipment. \n
			:return: trig_config: AAUT| UNCH AAUT The trigger settings are customized for the selected test case. The trigger setting 'Armed Auto' with external trigger source is used; the trigger delay is set to zero. Thus, the base station frame timing is able to synchronize the signal generator by a periodic trigger. UNCH The current trigger settings of the signal generator are retained unchanged.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:TRIGgerconfig?')
		return Conversions.str_to_scalar_enum(response, enums.TrigConf)

	def set_trigger_config(self, trig_config: enums.TrigConf) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:TRIGgerconfig \n
		Selects the trigger configuration. The trigger is used to synchronize the signal generator to the other equipment. \n
			:param trig_config: AAUT| UNCH AAUT The trigger settings are customized for the selected test case. The trigger setting 'Armed Auto' with external trigger source is used; the trigger delay is set to zero. Thus, the base station frame timing is able to synchronize the signal generator by a periodic trigger. UNCH The current trigger settings of the signal generator are retained unchanged.
		"""
		param = Conversions.enum_scalar_to_str(trig_config, enums.TrigConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:TRIGgerconfig {param}')
