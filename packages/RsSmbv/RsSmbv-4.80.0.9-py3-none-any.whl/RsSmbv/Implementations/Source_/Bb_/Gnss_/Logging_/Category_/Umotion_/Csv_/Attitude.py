from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attitude:
	"""Attitude commands group definition. 4 total commands, 3 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("attitude", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Attitude':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Attitude(self._core, self._base.parent)
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
	def acceleration(self):
		"""acceleration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acceleration'):
			from .Attitude_.Acceleration import Acceleration
			self._acceleration = Acceleration(self._core, self._base)
		return self._acceleration

	@property
	def jerk(self):
		"""jerk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_jerk'):
			from .Attitude_.Jerk import Jerk
			self._jerk = Jerk(self._core, self._base)
		return self._jerk

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Attitude_.Rate import Rate
			self._rate = Rate(self._core, self._base)
		return self._rate

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:[CSV]:ATTitude<CH> \n
		Enables the parameter for logging. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Attitude')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:CSV:ATTitude{channel_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:[CSV]:ATTitude<CH> \n
		Enables the parameter for logging. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Attitude')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:CSV:ATTitude{channel_cmd_val}?')
		return Conversions.str_to_bool(response)
