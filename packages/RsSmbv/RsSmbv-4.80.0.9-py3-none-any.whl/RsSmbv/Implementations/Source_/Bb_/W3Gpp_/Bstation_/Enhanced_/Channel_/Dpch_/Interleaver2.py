from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interleaver2:
	"""Interleaver2 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interleaver2", core, parent)

	def set(self, interleaver_2: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:INTerleaver2 \n
		The command activates or deactivates channel coding interleaver state 2 for the selected channel. Interleaver state 2 is
		activated or deactivated for all the transport channels together. Interleaver state 1 can be activated and deactivated
		for each transport channel individually (command method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Tchannel.
		Interleaver.set) . Note: The interleaver states do not cause the symbol rate to change. \n
			:param interleaver_2: ON| OFF
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(interleaver_2)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:INTerleaver2 {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:INTerleaver2 \n
		The command activates or deactivates channel coding interleaver state 2 for the selected channel. Interleaver state 2 is
		activated or deactivated for all the transport channels together. Interleaver state 1 can be activated and deactivated
		for each transport channel individually (command method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Tchannel.
		Interleaver.set) . Note: The interleaver states do not cause the symbol rate to change. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: interleaver_2: ON| OFF"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:INTerleaver2?')
		return Conversions.str_to_bool(response)
