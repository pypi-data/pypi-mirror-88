from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 14 total commands, 5 Sub-groups, 5 group commands"""

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
		"""output commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:RMODe \n
		No command help available \n
			:return: rm_ode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:SLENgth \n
		No command help available \n
			:return: slength: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:SLENgth \n
		No command help available \n
			:param slength: No help available
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlDvb:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:SLUNit \n
		No command help available \n
			:return: sl_unit: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlDvb)

	def set_sl_unit(self, sl_unit: enums.UnitSlDvb) -> None:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:SLUNit \n
		No command help available \n
			:param sl_unit: No help available
		"""
		param = Conversions.enum_scalar_to_str(sl_unit, enums.UnitSlDvb)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceB:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:SOURce \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceB)

	def set_source(self, source: enums.TriggerSourceB) -> None:
		"""[SOURce<HW>]:BB:PRAMp:TRIGger:SOURce \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:PRAMp:[TRIGger]:SEQuence \n
		No command help available \n
			:return: sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:PRAMp:[TRIGger]:SEQuence \n
		No command help available \n
			:param sequence: No help available
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:TRIGger:SEQuence {param}')
