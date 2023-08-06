from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 17 total commands, 4 Sub-groups, 5 group commands"""

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
		"""output commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Trigger_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""[SOURce<HW>]:BB:NFC:TRIGger:RMODe \n
		Queries the status of signal generation. \n
			:return: rm_ode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:NFC:TRIGger:SLENgth \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:return: slength: integer Range: 1 to 4294967295.0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:NFC:TRIGger:SLENgth \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:param slength: integer Range: 1 to 4294967295.0
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlB:
		"""[SOURce<HW>]:BB:NFC:TRIGger:SLUNit \n
		Defines the unit for the entry of the signal sequence length. \n
			:return: slunit: SEQuence| SAMPle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlB)

	def set_sl_unit(self, slunit: enums.UnitSlB) -> None:
		"""[SOURce<HW>]:BB:NFC:TRIGger:SLUNit \n
		Defines the unit for the entry of the signal sequence length. \n
			:param slunit: SEQuence| SAMPle
		"""
		param = Conversions.enum_scalar_to_str(slunit, enums.UnitSlB)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceA:
		"""[SOURce<HW>]:BB:NFC:TRIGger:SOURce \n
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
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceA)

	def set_source(self, source: enums.TriggerSourceA) -> None:
		"""[SOURce<HW>]:BB:NFC:TRIGger:SOURce \n
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
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:NFC:[TRIGger]:SEQuence \n
		Selects a reqular trigger mode. \n
			:return: sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:NFC:[TRIGger]:SEQuence \n
		Selects a reqular trigger mode. \n
			:param sequence: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TRIGger:SEQuence {param}')
