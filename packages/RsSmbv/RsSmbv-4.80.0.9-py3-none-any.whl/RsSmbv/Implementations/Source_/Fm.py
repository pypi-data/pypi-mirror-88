from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fm:
	"""Fm commands group definition. 10 total commands, 5 Sub-groups, 3 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fm", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Fm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_deviation'):
			from .Fm_.Deviation import Deviation
			self._deviation = Deviation(self._core, self._base)
		return self._deviation

	@property
	def external(self):
		"""external commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_external'):
			from .Fm_.External import External
			self._external = External(self._core, self._base)
		return self._external

	@property
	def internal(self):
		"""internal commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_internal'):
			from .Fm_.Internal import Internal
			self._internal = Internal(self._core, self._base)
		return self._internal

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Fm_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Fm_.State import State
			self._state = State(self._core, self._base)
		return self._state

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FmMode:
		"""[SOURce<HW>]:FM:MODE \n
		Selects the mode for the frequency modulation. \n
			:return: mode: HBANdwidth| LNOise HBANdwidth Selects maximum range for modulation bandwidth. LNOise Selects optimized phase noise and spurious characteristics with reduced modulation bandwidth and FM deviation.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FmMode)

	def set_mode(self, mode: enums.FmMode) -> None:
		"""[SOURce<HW>]:FM:MODE \n
		Selects the mode for the frequency modulation. \n
			:param mode: HBANdwidth| LNOise HBANdwidth Selects maximum range for modulation bandwidth. LNOise Selects optimized phase noise and spurious characteristics with reduced modulation bandwidth and FM deviation.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FmMode)
		self._core.io.write(f'SOURce<HwInstance>:FM:MODE {param}')

	def get_ratio(self) -> float:
		"""[SOURce<HW>]:FM:RATio \n
		Sets the deviation ratio (path2 to path1) in percent. \n
			:return: ratio: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""[SOURce<HW>]:FM:RATio \n
		Sets the deviation ratio (path2 to path1) in percent. \n
			:param ratio: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'SOURce<HwInstance>:FM:RATio {param}')

	def get_sensitivity(self) -> float:
		"""[SOURce<HW>]:FM:SENSitivity \n
		Queries the sensitivity of the externally supplied signal for frequency modulation. The sensitivity depends on the set
		modulation deviation. \n
			:return: sensitivity: float Sensitivity in Hz/V. It is assigned to the voltage value for full modulation of the input. Range: 0 to max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:SENSitivity?')
		return Conversions.str_to_float(response)
