from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 11 total commands, 5 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dattenuator(self):
		"""dattenuator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dattenuator'):
			from .Power_.Dattenuator import Dattenuator
			self._dattenuator = Dattenuator(self._core, self._base)
		return self._dattenuator

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Power_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .Power_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def spacing(self):
		"""spacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spacing'):
			from .Power_.Spacing import Spacing
			self._spacing = Spacing(self._core, self._base)
		return self._spacing

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Power_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def get_dwell(self) -> float:
		"""[SOURce<HW>]:SWEep:POWer:DWELl \n
		Sets the dwell time for a level sweep step. \n
			:return: dwell: float Range: 0.001 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:DWELl?')
		return Conversions.str_to_float(response)

	def set_dwell(self, dwell: float) -> None:
		"""[SOURce<HW>]:SWEep:POWer:DWELl \n
		Sets the dwell time for a level sweep step. \n
			:param dwell: float Range: 0.001 to 100
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:DWELl {param}')

	def get_points(self) -> int:
		"""[SOURce<HW>]:SWEep:POWer:POINts \n
		Sets the number of steps within the RF level sweep range. See 'Correlating Parameters in Sweep Mode'. \n
			:return: points: integer Range: 2 to Max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:POINts?')
		return Conversions.str_to_int(response)

	def set_points(self, points: int) -> None:
		"""[SOURce<HW>]:SWEep:POWer:POINts \n
		Sets the number of steps within the RF level sweep range. See 'Correlating Parameters in Sweep Mode'. \n
			:param points: integer Range: 2 to Max
		"""
		param = Conversions.decimal_value_to_str(points)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:POINts {param}')

	def get_retrace(self) -> bool:
		"""[SOURce<HW>]:SWEep:POWer:RETRace \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:RETRace?')
		return Conversions.str_to_bool(response)

	def set_retrace(self, state: bool) -> None:
		"""[SOURce<HW>]:SWEep:POWer:RETRace \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:RETRace {param}')

	def get_running(self) -> bool:
		"""[SOURce<HW>]:SWEep:POWer:RUNNing \n
		Queries the current sweep state. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:RUNNing?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.SweCyclMode:
		"""[SOURce<HW>]:SWEep:POWer:SHAPe \n
		Determines the waveform shape for a frequency sweep sequence. \n
			:return: shape: SAWTooth| TRIangle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.SweCyclMode)

	def set_shape(self, shape: enums.SweCyclMode) -> None:
		"""[SOURce<HW>]:SWEep:POWer:SHAPe \n
		Determines the waveform shape for a frequency sweep sequence. \n
			:param shape: SAWTooth| TRIangle
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.SweCyclMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:SHAPe {param}')
