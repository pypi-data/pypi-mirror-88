from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insert", core, parent)

	def set(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:AREA<CH>:INSert \n
		Appends, insertes or deletes an obscured zone. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:AREA{channel_cmd_val}:INSert')

	def set_with_opc(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:AREA<CH>:INSert \n
		Appends, insertes or deletes an obscured zone. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:AREA{channel_cmd_val}:INSert')
