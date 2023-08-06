from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rlm:
	"""Rlm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: RlmPart, default value after init: RlmPart.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rlm", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_rlmPart_get', 'repcap_rlmPart_set', repcap.RlmPart.Nr1)

	def clone(self) -> 'Rlm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rlm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_rlmPart_set(self, enum_value: repcap.RlmPart) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RlmPart.Default
		Default value after init: RlmPart.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_rlmPart_get(self) -> repcap.RlmPart:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, sar_rlm_data: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, rlmPart=repcap.RlmPart.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:NMESsage:INAV:EPHemeris:SAR:RLM<S2US> \n
		Sets the 20-bit Search-and-Rescue Service (SAR) return link message (RLM) data for nominal mode operation.
		For more information, refer to specification . \n
			:param sar_rlm_data: integer Range: 0 to 1048575
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param rlmPart: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rlm')"""
		param = Conversions.decimal_value_to_str(sar_rlm_data)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		rlmPart_cmd_val = self._base.get_repcap_cmd_value(rlmPart, repcap.RlmPart)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:NMESsage:INAV:EPHemeris:SAR:RLM{rlmPart_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, rlmPart=repcap.RlmPart.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:NMESsage:INAV:EPHemeris:SAR:RLM<S2US> \n
		Sets the 20-bit Search-and-Rescue Service (SAR) return link message (RLM) data for nominal mode operation.
		For more information, refer to specification . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:param rlmPart: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rlm')
			:return: sar_rlm_data: integer Range: 0 to 1048575"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		rlmPart_cmd_val = self._base.get_repcap_cmd_value(rlmPart, repcap.RlmPart)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:NMESsage:INAV:EPHemeris:SAR:RLM{rlmPart_cmd_val}?')
		return Conversions.str_to_int(response)
