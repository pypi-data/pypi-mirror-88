from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class External:
	"""External commands group definition. 5 total commands, 3 Sub-groups, 2 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("external", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'External':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = External(self._core, self._base.parent)
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
	def rdelay(self):
		"""rdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdelay'):
			from .External_.Rdelay import Rdelay
			self._rdelay = Rdelay(self._core, self._base)
		return self._rdelay

	@property
	def synchronize(self):
		"""synchronize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronize'):
			from .External_.Synchronize import Synchronize
			self._synchronize = Synchronize(self._core, self._base)
		return self._synchronize

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .External_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:TRIGger:[EXTernal]:DELay \n
		Sets the trigger delay. \n
			:return: delay: float Range: 0 to 1099511627774, Unit: Samples
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TRIGger:EXTernal:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TRIGger:[EXTernal]:DELay \n
		Sets the trigger delay. \n
			:param delay: float Range: 0 to 1099511627774, Unit: Samples
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:EXTernal:DELay {param}')

	def get_inhibit(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TRIGger:[EXTernal]:INHibit \n
		Specifies the number of symbols by which a restart is inhibited. \n
			:return: inhibit: integer Range: 0 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TRIGger:EXTernal:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TRIGger:[EXTernal]:INHibit \n
		Specifies the number of symbols by which a restart is inhibited. \n
			:param inhibit: integer Range: 0 to dynamic
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:EXTernal:INHibit {param}')
