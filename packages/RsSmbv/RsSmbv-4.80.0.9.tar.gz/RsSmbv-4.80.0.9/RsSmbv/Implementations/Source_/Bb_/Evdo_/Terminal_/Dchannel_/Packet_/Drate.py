from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Drate:
	"""Drate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("drate", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:DRATe \n
		(enabled for an access terminal working in traffic mode) Displays the data rate in kbps of the selected packet.
		Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for
		physical layer subtype 2. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: drate: float Range: 0 to ..."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:DRATe?')
		return Conversions.str_to_float(response)
