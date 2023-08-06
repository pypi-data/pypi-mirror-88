from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 19 total commands, 5 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def arm(self):
		"""arm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arm'):
			from .Trigger_.Arm import Arm
			self._arm = Arm(self._core, self._base)
		return self._arm

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Trigger_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def external(self):
		"""external commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_external'):
			from .Trigger_.External import External
			self._external = External(self._core, self._base)
		return self._external

	@property
	def obaseband(self):
		"""obaseband commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_obaseband'):
			from .Trigger_.Obaseband import Obaseband
			self._obaseband = Obaseband(self._core, self._base)
		return self._obaseband

	@property
	def output(self):
		"""output commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:RMODe \n
		No command help available \n
			:return: rm_ode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:SLENgth \n
		No command help available \n
			:return: slength: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:SLENgth?')
		return Conversions.str_to_float(response)

	def set_slength(self, slength: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:SLENgth \n
		No command help available \n
			:param slength: No help available
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlA:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:SLUNit \n
		No command help available \n
			:return: slunit: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlA)

	def set_sl_unit(self, slunit: enums.UnitSlA) -> None:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:SLUNit \n
		No command help available \n
			:param slunit: No help available
		"""
		param = Conversions.enum_scalar_to_str(slunit, enums.UnitSlA)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceB:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:SOURce \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceB)

	def set_source(self, source: enums.TriggerSourceB) -> None:
		"""[SOURce<HW>]:BB:WLAN:TRIGger:SOURce \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:WLAN:[TRIGger]:SEQuence \n
		No command help available \n
			:return: sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:WLAN:[TRIGger]:SEQuence \n
		No command help available \n
			:param sequence: No help available
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:SEQuence {param}')
