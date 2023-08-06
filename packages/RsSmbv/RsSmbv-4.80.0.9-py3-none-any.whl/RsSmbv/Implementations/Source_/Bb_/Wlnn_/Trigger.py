from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 24 total commands, 4 Sub-groups, 5 group commands"""

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
	def output(self):
		"""output commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:RMODe \n
		The command queries the current status of signal generation for all trigger modes with IEEE 802.11 WLAN modulation on. \n
			:return: rm_ode: RUN| STOP RUN the signal is generated. A trigger event occurred in the triggered mode. STOP the signal is not generated. A trigger event did not occur in the triggered modes, or signal generation was stopped by the command :BB:WLNN:TRIG:ARM:EXECute (armed trigger modes only) .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:SLENgth \n
		The command defines the length of the signal sequence to be output in the 'Single' trigger mode (BB:SEQuence is set to
		SING) . The input is made in terms of samples. It is possible to output deliberately just part of the frame, an exact
		sequence of the frame, or a defined number of repetitions of the frame. \n
			:return: slength: integer Range: 1 to (2^32) - 1, Unit: sample
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:SLENgth \n
		The command defines the length of the signal sequence to be output in the 'Single' trigger mode (BB:SEQuence is set to
		SING) . The input is made in terms of samples. It is possible to output deliberately just part of the frame, an exact
		sequence of the frame, or a defined number of repetitions of the frame. \n
			:param slength: integer Range: 1 to (2^32) - 1, Unit: sample
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlB:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:SLUNit \n
		Defines the unit for the entry of the length of the signal sequence (method RsSmbv.Source.Bb.Wlnn.Trigger.slength) to be
		output in the single trigger mode (BB:SEQuence is set to SINGle) . \n
			:return: slunit: SAMPle| SEQuence SAMPle Unit Sample. A single sample is generated after a trigger event. SEQuence Unit Sequence Length. A single sequence is generated after a trigger event.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlB)

	def set_sl_unit(self, slunit: enums.UnitSlB) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:SLUNit \n
		Defines the unit for the entry of the length of the signal sequence (method RsSmbv.Source.Bb.Wlnn.Trigger.slength) to be
		output in the single trigger mode (BB:SEQuence is set to SINGle) . \n
			:param slunit: SAMPle| SEQuence SAMPle Unit Sample. A single sample is generated after a trigger event. SEQuence Unit Sequence Length. A single sequence is generated after a trigger event.
		"""
		param = Conversions.enum_scalar_to_str(slunit, enums.UnitSlB)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceA:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:SOURce \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceA)

	def set_source(self, source: enums.TriggerSourceA) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:SOURce \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TriggerSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:WLNN:[TRIGger]:SEQuence \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single \n
			:return: sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:WLNN:[TRIGger]:SEQuence \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single \n
			:param sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:SEQuence {param}')
