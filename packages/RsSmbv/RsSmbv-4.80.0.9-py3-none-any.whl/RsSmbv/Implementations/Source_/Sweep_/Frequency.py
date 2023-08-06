from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 11 total commands, 3 Sub-groups, 6 group commands"""

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
		"""[SOURce<HW>]:SWEep:[FREQuency]:DWELl \n
		Sets the dwell time for a frequency sweep step. \n
			:return: dwell: float Range: 0.001 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:DWELl?')
		return Conversions.str_to_float(response)

	def set_dwell(self, dwell: float) -> None:
		"""[SOURce<HW>]:SWEep:[FREQuency]:DWELl \n
		Sets the dwell time for a frequency sweep step. \n
			:param dwell: float Range: 0.001 to 100
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:DWELl {param}')

	def get_points(self) -> int:
		"""[SOURce<HW>]:SWEep:[FREQuency]:POINts \n
		Sets the number of steps within the RF frequency sweep range. See 'Correlating Parameters in Sweep Mode'. Two separate
		POINts values are used for linear or logarithmic sweep spacing (LIN | LOG) . The command always affects the currently set
		sweep spacing. \n
			:return: points: integer Range: 2 to Max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:POINts?')
		return Conversions.str_to_int(response)

	def set_points(self, points: int) -> None:
		"""[SOURce<HW>]:SWEep:[FREQuency]:POINts \n
		Sets the number of steps within the RF frequency sweep range. See 'Correlating Parameters in Sweep Mode'. Two separate
		POINts values are used for linear or logarithmic sweep spacing (LIN | LOG) . The command always affects the currently set
		sweep spacing. \n
			:param points: integer Range: 2 to Max
		"""
		param = Conversions.decimal_value_to_str(points)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:POINts {param}')

	def get_retrace(self) -> bool:
		"""[SOURce<HW>]:SWEep:[FREQuency]:RETRace \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:RETRace?')
		return Conversions.str_to_bool(response)

	def set_retrace(self, state: bool) -> None:
		"""[SOURce<HW>]:SWEep:[FREQuency]:RETRace \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:RETRace {param}')

	def get_running(self) -> bool:
		"""[SOURce<HW>]:SWEep:[FREQuency]:RUNNing \n
		Queries the current sweep state. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:RUNNing?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.SweCyclMode:
		"""[SOURce<HW>]:SWEep:[FREQuency]:SHAPe \n
		Determines the waveform shape for a frequency sweep sequence. \n
			:return: shape: SAWTooth| TRIangle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.SweCyclMode)

	def set_shape(self, shape: enums.SweCyclMode) -> None:
		"""[SOURce<HW>]:SWEep:[FREQuency]:SHAPe \n
		Determines the waveform shape for a frequency sweep sequence. \n
			:param shape: SAWTooth| TRIangle
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.SweCyclMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:SHAPe {param}')

	# noinspection PyTypeChecker
	def get_spacing(self) -> enums.Spacing:
		"""[SOURce<HW>]:SWEep:[FREQuency]:SPACing \n
		Selects the mode for the calculation of the frequency intervals, with which the current frequency at each step is
		increased or decreased. The keyword [:FREQuency] can be omitted; then the command is SCPI-compliant. \n
			:return: spacing: LINear| LOGarithmic LINear Sets a fixed frequency value as step width and adds it to the current frequency. The linear step width is entered in Hz, see [:​SOURcehw]:​SWEep[:​FREQuency]:​STEP[:​LINear]. LOGarithmic Sets a constant fraction of the current frequency as step width and adds it to the current frequency. The logarithmic step width is entered in %, see STEP:LOGarithmic.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:SPACing?')
		return Conversions.str_to_scalar_enum(response, enums.Spacing)

	def set_spacing(self, spacing: enums.Spacing) -> None:
		"""[SOURce<HW>]:SWEep:[FREQuency]:SPACing \n
		Selects the mode for the calculation of the frequency intervals, with which the current frequency at each step is
		increased or decreased. The keyword [:FREQuency] can be omitted; then the command is SCPI-compliant. \n
			:param spacing: LINear| LOGarithmic LINear Sets a fixed frequency value as step width and adds it to the current frequency. The linear step width is entered in Hz, see [:​SOURcehw]:​SWEep[:​FREQuency]:​STEP[:​LINear]. LOGarithmic Sets a constant fraction of the current frequency as step width and adds it to the current frequency. The logarithmic step width is entered in %, see STEP:LOGarithmic.
		"""
		param = Conversions.enum_scalar_to_str(spacing, enums.Spacing)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:SPACing {param}')
