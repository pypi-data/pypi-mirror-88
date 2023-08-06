from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Burst:
	"""Burst commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("burst", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Burst':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Burst(self._core, self._base.parent)
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

	def set(self, burst_length: enums.WcdmaUlDtxBurstLen, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:BURSt<CH> \n
		Determines the uplink DPCCH burst length in subframes without the preamble and postamble, when the corresponding UE-DTX
		cycle is applied. \n
			:param burst_length: 1| 2| 5
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')"""
		param = Conversions.enum_scalar_to_str(burst_length, enums.WcdmaUlDtxBurstLen)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:BURSt{channel_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WcdmaUlDtxBurstLen:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:BURSt<CH> \n
		Determines the uplink DPCCH burst length in subframes without the preamble and postamble, when the corresponding UE-DTX
		cycle is applied. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')
			:return: burst_length: 1| 2| 5"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:BURSt{channel_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.WcdmaUlDtxBurstLen)
