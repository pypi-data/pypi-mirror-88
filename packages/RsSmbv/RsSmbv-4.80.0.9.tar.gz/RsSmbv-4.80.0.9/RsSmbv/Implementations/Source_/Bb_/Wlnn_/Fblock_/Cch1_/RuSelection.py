from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RuSelection:
	"""RuSelection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ruSelection", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'RuSelection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RuSelection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, ru_sel_ch_1: enums.WlannFbPpduRuSel, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:CCH1:RUSelection<ST> \n
		Sets the the resource unit of the first content channel for the respective channel and station. \n
			:param ru_sel_ch_1: RU0| RU1| RU2| RU3| RU4| RU5| RU6| RU7| RU8| RU9| RU10| RU11| RU12| RU13| RU14| RU15| RU18| RU19| RU20| RU21| RU22| RU23| RU24| RU25| RU34| RU35| RU36| RU37| RU38| RU16| RU17| RU26| RU27| RU28| RU29| RU30| RU31| RU32| RU33
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RuSelection')"""
		param = Conversions.enum_scalar_to_str(ru_sel_ch_1, enums.WlannFbPpduRuSel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:CCH1:RUSelection{stream_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.WlannFbPpduRuSel:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:CCH1:RUSelection<ST> \n
		Sets the the resource unit of the first content channel for the respective channel and station. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RuSelection')
			:return: ru_sel_ch_1: RU0| RU1| RU2| RU3| RU4| RU5| RU6| RU7| RU8| RU9| RU10| RU11| RU12| RU13| RU14| RU15| RU18| RU19| RU20| RU21| RU22| RU23| RU24| RU25| RU34| RU35| RU36| RU37| RU38| RU16| RU17| RU26| RU27| RU28| RU29| RU30| RU31| RU32| RU33"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:CCH1:RUSelection{stream_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpduRuSel)
