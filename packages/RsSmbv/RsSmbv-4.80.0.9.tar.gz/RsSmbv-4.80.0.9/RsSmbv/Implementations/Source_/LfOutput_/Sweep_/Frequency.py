from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 12 total commands, 3 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Frequency_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .Frequency_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Frequency_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def get_dwell(self) -> float:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:DWELl \n
		Sets the dwell time for each frequency step of the sweep. \n
			:return: dwell: float Range: 0.001 to 100, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:DWELl?')
		return Conversions.str_to_float(response)

	def set_dwell(self, dwell: float) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:DWELl \n
		Sets the dwell time for each frequency step of the sweep. \n
			:param dwell: float Range: 0.001 to 100, Unit: s
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:DWELl {param}')

	# noinspection PyTypeChecker
	def get_lf_source(self) -> enums.LfSweepSource:
		"""[SOURce]:LFOutput:SWEep:[FREQuency]:LFSource \n
		No command help available \n
			:return: lf_source: No help available
		"""
		response = self._core.io.query_str('SOURce:LFOutput:SWEep:FREQuency:LFSource?')
		return Conversions.str_to_scalar_enum(response, enums.LfSweepSource)

	def set_lf_source(self, lf_source: enums.LfSweepSource) -> None:
		"""[SOURce]:LFOutput:SWEep:[FREQuency]:LFSource \n
		No command help available \n
			:param lf_source: No help available
		"""
		param = Conversions.enum_scalar_to_str(lf_source, enums.LfSweepSource)
		self._core.io.write(f'SOURce:LFOutput:SWEep:FREQuency:LFSource {param}')

	def get_points(self) -> int:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:POINts \n
		Sets the number of steps in an LF sweep. For information on how the value is calculated and the interdependency with
		other parameters, see 'Correlating Parameters in Sweep Mode' \n
			:return: points: integer Range: 2 to POINts
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:POINts?')
		return Conversions.str_to_int(response)

	def set_points(self, points: int) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:POINts \n
		Sets the number of steps in an LF sweep. For information on how the value is calculated and the interdependency with
		other parameters, see 'Correlating Parameters in Sweep Mode' \n
			:param points: integer Range: 2 to POINts
		"""
		param = Conversions.decimal_value_to_str(points)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:POINts {param}')

	def get_retrace(self) -> bool:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:RETRace \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:RETRace?')
		return Conversions.str_to_bool(response)

	def set_retrace(self, state: bool) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:RETRace \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:RETRace {param}')

	def get_running(self) -> bool:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:RUNNing \n
		Queries the current status of the LF frequency sweep mode. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:RUNNing?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.SweCyclMode:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:SHAPe \n
		Sets the cycle mode for a sweep sequence (shape) . \n
			:return: shape: SAWTooth| TRIangle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.SweCyclMode)

	def set_shape(self, shape: enums.SweCyclMode) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:SHAPe \n
		Sets the cycle mode for a sweep sequence (shape) . \n
			:param shape: SAWTooth| TRIangle
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.SweCyclMode)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:SHAPe {param}')

	# noinspection PyTypeChecker
	def get_spacing(self) -> enums.Spacing:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:SPACing \n
		Selects linear or logarithmic sweep spacing. \n
			:return: spacing: LINear| LOGarithmic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:SPACing?')
		return Conversions.str_to_scalar_enum(response, enums.Spacing)

	def set_spacing(self, spacing: enums.Spacing) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:SPACing \n
		Selects linear or logarithmic sweep spacing. \n
			:param spacing: LINear| LOGarithmic
		"""
		param = Conversions.enum_scalar_to_str(spacing, enums.Spacing)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:SPACing {param}')
