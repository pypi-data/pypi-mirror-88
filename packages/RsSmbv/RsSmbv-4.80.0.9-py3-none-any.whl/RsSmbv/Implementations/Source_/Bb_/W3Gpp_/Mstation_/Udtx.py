from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Udtx:
	"""Udtx commands group definition. 18 total commands, 6 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("udtx", core, parent)

	def clone(self) -> 'Udtx':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Udtx(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def burst(self):
		"""burst commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_burst'):
			from .Udtx_.Burst import Burst
			self._burst = Burst(self._core, self._base)
		return self._burst

	@property
	def cycle(self):
		"""cycle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycle'):
			from .Udtx_.Cycle import Cycle
			self._cycle = Cycle(self._core, self._base)
		return self._cycle

	@property
	def dpcc(self):
		"""dpcc commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_dpcc'):
			from .Udtx_.Dpcc import Dpcc
			self._dpcc = Dpcc(self._core, self._base)
		return self._dpcc

	@property
	def postamble(self):
		"""postamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_postamble'):
			from .Udtx_.Postamble import Postamble
			self._postamble = Postamble(self._core, self._base)
		return self._postamble

	@property
	def preamble(self):
		"""preamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preamble'):
			from .Udtx_.Preamble import Preamble
			self._preamble = Preamble(self._core, self._base)
		return self._preamble

	@property
	def usch(self):
		"""usch commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_usch'):
			from .Udtx_.Usch import Usch
			self._usch = Usch(self._core, self._base)
		return self._usch

	# noinspection PyTypeChecker
	def get_ithreshold(self) -> enums.WcdmaUlDtxThreshold:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:ITHReshold \n
		Defines the number of consecutive E-DCH TTIs without an E-DCH transmission, after which the UE shall immediately move
		from UE-DTX cycle 1 to using UE-DTX cycle 2. \n
			:return: threshold: 1| 4| 8| 16| 32| 64| 128| 256
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:ITHReshold?')
		return Conversions.str_to_scalar_enum(response, enums.WcdmaUlDtxThreshold)

	def set_ithreshold(self, threshold: enums.WcdmaUlDtxThreshold) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:ITHReshold \n
		Defines the number of consecutive E-DCH TTIs without an E-DCH transmission, after which the UE shall immediately move
		from UE-DTX cycle 1 to using UE-DTX cycle 2. \n
			:param threshold: 1| 4| 8| 16| 32| 64| 128| 256
		"""
		param = Conversions.enum_scalar_to_str(threshold, enums.WcdmaUlDtxThreshold)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:ITHReshold {param}')

	# noinspection PyTypeChecker
	def get_lp_length(self) -> enums.WcdmaUlDtxLongPreLen:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:LPLength \n
		Determines the length in slots of the preamble associated with the UE-DTX cycle 2. \n
			:return: long_preamble: 2| 4| 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:LPLength?')
		return Conversions.str_to_scalar_enum(response, enums.WcdmaUlDtxLongPreLen)

	def set_lp_length(self, long_preamble: enums.WcdmaUlDtxLongPreLen) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:LPLength \n
		Determines the length in slots of the preamble associated with the UE-DTX cycle 2. \n
			:param long_preamble: 2| 4| 15
		"""
		param = Conversions.enum_scalar_to_str(long_preamble, enums.WcdmaUlDtxLongPreLen)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:LPLength {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.WcdmaUlDtxMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:MODE \n
		The mode is fixed to UL-DTX. \n
			:return: uldtx_mode: UDTX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.WcdmaUlDtxMode)

	def set_mode(self, uldtx_mode: enums.WcdmaUlDtxMode) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:MODE \n
		The mode is fixed to UL-DTX. \n
			:param uldtx_mode: UDTX
		"""
		param = Conversions.enum_scalar_to_str(uldtx_mode, enums.WcdmaUlDtxMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:MODE {param}')

	def get_offset(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:OFFSet \n
		Sets the parameter UE_DTX_DRX_Offset and determines the start offset in subframes of the first uplink DPCCH burst (after
		the preamble) . The offset is applied only for bursts belonging to the DPCCH burst pattern; HS-DPCCH or E-DCH
		transmissions are not affected. \n
			:return: offset: integer Range: 0 to 159
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:OFFSet?')
		return Conversions.str_to_int(response)

	def set_offset(self, offset: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:OFFSet \n
		Sets the parameter UE_DTX_DRX_Offset and determines the start offset in subframes of the first uplink DPCCH burst (after
		the preamble) . The offset is applied only for bursts belonging to the DPCCH burst pattern; HS-DPCCH or E-DCH
		transmissions are not affected. \n
			:param offset: integer Range: 0 to 159
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:OFFSet {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:STATe \n
		Enables/disables UL-DTX. Enabling the UL-DTX deactivates the DPDCH and the HSUPA FRC. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:STATe \n
		Enables/disables UL-DTX. Enabling the UL-DTX deactivates the DPDCH and the HSUPA FRC. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:STATe {param}')

	# noinspection PyTypeChecker
	def get_ttiedch(self) -> enums.HsUpaDchTti:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:TTIEdch \n
		Sets the duration of a E-DCH TTI. \n
			:return: edch_tti: 2ms| 10ms Range: 2ms to 10ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:TTIEdch?')
		return Conversions.str_to_scalar_enum(response, enums.HsUpaDchTti)

	def set_ttiedch(self, edch_tti: enums.HsUpaDchTti) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:TTIEdch \n
		Sets the duration of a E-DCH TTI. \n
			:param edch_tti: 2ms| 10ms Range: 2ms to 10ms
		"""
		param = Conversions.enum_scalar_to_str(edch_tti, enums.HsUpaDchTti)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:TTIEdch {param}')
