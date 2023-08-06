from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EvdoModulation:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:MODulation \n
		(enabled for physical layer subtype 2 and for an access terminal working in traffic mode) Displays the modulation type
		per packet. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: modulation: B4| Q4| Q2| Q4Q2| E4E2 B4 The modulation type is set to BPSK modulation with 4-ary Walsh cover. Q4 The modulation type is set to QPSK modulation with 4-ary Walsh cover. Q2 The modulation type is set to QPSK modulation with 2-ary Walsh cover. Q4Q2 Sum of Q4 and Q2 modulated symbols. E4E2 Sum of E4 (8-PSK modulated with 4-ary Walsh cover) and E2 (8-PSK modulated with 2-ary Walsh cover) modulated symbols."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoModulation)
