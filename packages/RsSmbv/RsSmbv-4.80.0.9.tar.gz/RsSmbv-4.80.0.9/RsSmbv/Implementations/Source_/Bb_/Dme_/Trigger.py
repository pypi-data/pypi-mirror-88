from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 9 total commands, 3 Sub-groups, 4 group commands"""

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

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""[SOURce<HW>]:BB:DME:TRIGger:RMODe \n
		Queries the signal generation status. \n
			:return: run_mode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:DME:TRIGger:SLENgth \n
		Defines the length of the signal sequence that is output in the SINGle trigger mode. \n
			:return: seq_length: integer Range: 1 samples to 2^32-1 samples
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, seq_length: int) -> None:
		"""[SOURce<HW>]:BB:DME:TRIGger:SLENgth \n
		Defines the length of the signal sequence that is output in the SINGle trigger mode. \n
			:param seq_length: integer Range: 1 samples to 2^32-1 samples
		"""
		param = Conversions.decimal_value_to_str(seq_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceA:
		"""[SOURce<HW>]:BB:DME:TRIGger:SOURce \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: trigger_source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceA)

	def set_source(self, trigger_source: enums.TriggerSourceA) -> None:
		"""[SOURce<HW>]:BB:DME:TRIGger:SOURce \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors
			Table Header:  \n
			- EGT1: External global trigger
			- EGC1: External global clock
			- In master-slave mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde
		& Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param trigger_source: INTernal| EGT1| EGC1| EXTernal| BBSY
		"""
		param = Conversions.enum_scalar_to_str(trigger_source, enums.TriggerSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:DME:[TRIGger]:SEQuence \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single \n
			:return: trigger_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, trigger_mode: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:DME:[TRIGger]:SEQuence \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single \n
			:param trigger_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(trigger_mode, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:TRIGger:SEQuence {param}')
