from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpControl:
	"""DpControl commands group definition. 9 total commands, 2 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpControl", core, parent)

	def clone(self) -> 'DpControl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpControl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_range'):
			from .DpControl_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .DpControl_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	# noinspection PyTypeChecker
	def get_assignment(self) -> enums.PowContAssMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:ASSignment \n
		Enabled for UL-DTX mode only (method RsSmbv.Source.Bb.W3Gpp.Mstation.Udtx.state ON) . The power control recognizes the
		UL-DPCCH gaps according to 3GPP TS 25.214. Some of the TPC commands sent to the instrument over the external line or by
		the TPC pattern are ignored, whereas others are summed up and applied later. The processing of the TPC commands depends
		only on whether the BS sends the TPC bits on the F-DPCH with slot format 0/ slot format 9 or not. \n
			:return: assignment: NORMal| FDPCh
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:ASSignment?')
		return Conversions.str_to_scalar_enum(response, enums.PowContAssMode)

	def set_assignment(self, assignment: enums.PowContAssMode) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:ASSignment \n
		Enabled for UL-DTX mode only (method RsSmbv.Source.Bb.W3Gpp.Mstation.Udtx.state ON) . The power control recognizes the
		UL-DPCCH gaps according to 3GPP TS 25.214. Some of the TPC commands sent to the instrument over the external line or by
		the TPC pattern are ignored, whereas others are summed up and applied later. The processing of the TPC commands depends
		only on whether the BS sends the TPC bits on the F-DPCH with slot format 0/ slot format 9 or not. \n
			:param assignment: NORMal| FDPCh
		"""
		param = Conversions.enum_scalar_to_str(assignment, enums.PowContAssMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:ASSignment {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.UpDownDirection:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:DIRection \n
		The command selects the Dynamic Power Control direction. The selected direction determines if the channel power is
		increased (UP) or decreased (DOWN) by control signal with high level. \n
			:return: direction: UP| DOWN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.UpDownDirection)

	def set_direction(self, direction: enums.UpDownDirection) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:DIRection \n
		The command selects the Dynamic Power Control direction. The selected direction determines if the channel power is
		increased (UP) or decreased (DOWN) by control signal with high level. \n
			:param direction: UP| DOWN
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.UpDownDirection)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:DIRection {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PowContMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:MODE \n
		Determines the source of the control signal. \n
			:return: mode: TPC| MANual
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PowContMode)

	def set_mode(self, mode: enums.PowContMode) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:MODE \n
		Determines the source of the control signal. \n
			:param mode: TPC| MANual
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PowContMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:MODE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:STATe \n
		Activates/deactivates Dynamic Power Control. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:STATe \n
		Activates/deactivates Dynamic Power Control. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:STATe {param}')

	def get_power(self) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:[POWer] \n
		The command queries the deviation of the channel power (delta POW) from the set power start value of the DPDCH. \n
			:return: power: float Range: -60 to 60
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:POWer?')
		return Conversions.str_to_float(response)
