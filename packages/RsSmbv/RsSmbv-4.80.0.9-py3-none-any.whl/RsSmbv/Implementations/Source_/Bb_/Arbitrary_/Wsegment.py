from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wsegment:
	"""Wsegment commands group definition. 23 total commands, 3 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wsegment", core, parent)

	def clone(self) -> 'Wsegment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Wsegment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def configure(self):
		"""configure commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_configure'):
			from .Wsegment_.Configure import Configure
			self._configure = Configure(self._core, self._base)
		return self._configure

	@property
	def next(self):
		"""next commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_next'):
			from .Wsegment_.Next import Next
			self._next = Next(self._core, self._base)
		return self._next

	@property
	def sequence(self):
		"""sequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sequence'):
			from .Wsegment_.Sequence import Sequence
			self._sequence = Sequence(self._core, self._base)
		return self._sequence

	def set_cload(self, filename_input: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CLOad \n
		Creates a multi-segment waveform using the current entries of the specified configuration file (*.inf_mswv) . The ARB
		generator is activated, the new multi-segment waveform (*.wv) is loaded and the first segment is output in accordance to
		the trigger settings. \n
			:param filename_input: string Absolute file path, file name of the configuration file and file extension (*.inf_mswv)
		"""
		param = Conversions.value_to_quoted_str(filename_input)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CLOad {param}')

	def set_create(self, filename_input: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CREate \n
		Creates a multi-segment waveform (*.wv) using the current settings of the specified configuration file (*.inf_mswv) . \n
			:param filename_input: Absolute file path, file name of the configuration file and file extension (*.inf_mswv)
		"""
		param = Conversions.value_to_quoted_str(filename_input)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CREate {param}')

	# noinspection PyTypeChecker
	def get_lmode(self) -> enums.ArbLevMode:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:LMODe \n
		Sets how the segments are leveled. \n
			:return: level_mode: HIGHest| UNCHanged
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:LMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ArbLevMode)

	def set_lmode(self, level_mode: enums.ArbLevMode) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:LMODe \n
		Sets how the segments are leveled. \n
			:param level_mode: HIGHest| UNCHanged
		"""
		param = Conversions.enum_scalar_to_str(level_mode, enums.ArbLevMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:LMODe {param}')

	def get_name(self) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:NAME \n
		Queries the name of the waveform of the currently output segment of the multi-segment waveform. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:NAME?')
		return trim_str_response(response)

	def get_value(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment \n
		Queries the index of the currently processed segment. \n
			:return: wsegment: integer Range: 0 to 1023
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment?')
		return Conversions.str_to_int(response)
