from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 21 total commands, 5 Sub-groups, 4 group commands"""

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
		"""external commands group. 1 Sub-classes, 2 commands."""
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
		"""output commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:RMODe \n
		Queries the status of waveform output. \n
			:return: rm_ode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:SLENgth \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:return: slength: float Range: 0.001 to 46.648730700, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TRIGger:SLENgth?')
		return Conversions.str_to_float(response)

	def set_slength(self, slength: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:SLENgth \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:param slength: float Range: 0.001 to 46.648730700, Unit: s
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceC:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:SOURce \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: source: INTernal| EGT1| EXTernal| EGC1| BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceC)

	def set_source(self, source: enums.TriggerSourceC) -> None:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:SOURce \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param source: INTernal| EGT1| EXTernal| EGC1| BBSY
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceC)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:GNSS:[TRIGger]:SEQuence \n
		Selects the trigger mode. \n
			:return: sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:GNSS:[TRIGger]:SEQuence \n
		Selects the trigger mode. \n
			:param sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:SEQuence {param}')
