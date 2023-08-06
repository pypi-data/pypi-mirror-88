from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvParameter:
	"""RvParameter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TwoStreams, default value after init: TwoStreams.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvParameter", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_twoStreams_get', 'repcap_twoStreams_set', repcap.TwoStreams.Nr0)

	def clone(self) -> 'RvParameter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RvParameter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_twoStreams_set(self, enum_value: repcap.TwoStreams) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TwoStreams.Default
		Default value after init: TwoStreams.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_twoStreams_get(self) -> repcap.TwoStreams:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, rv_parameter: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:RVParameter<DI> \n
		The parameter is enabled for 'HARQ Simulation Mode' set to Constant ACK. The command sets the Redundancy Version
		Parameter. This value determines the processing of the Forward Error Correction and Constellation Arrangement (QAM16 and
		64QAM modulation) , see TS 25.212 4.6.2. For HS-SCCH Type 2 (less operation) , the Redundancy Version Parameter is always
		0. \n
			:param rv_parameter: integer Range: 0 to 7
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'RvParameter')"""
		param = Conversions.decimal_value_to_str(rv_parameter)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:RVParameter{twoStreams_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:RVParameter<DI> \n
		The parameter is enabled for 'HARQ Simulation Mode' set to Constant ACK. The command sets the Redundancy Version
		Parameter. This value determines the processing of the Forward Error Correction and Constellation Arrangement (QAM16 and
		64QAM modulation) , see TS 25.212 4.6.2. For HS-SCCH Type 2 (less operation) , the Redundancy Version Parameter is always
		0. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'RvParameter')
			:return: rv_parameter: integer Range: 0 to 7"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:RVParameter{twoStreams_cmd_val}?')
		return Conversions.str_to_int(response)
