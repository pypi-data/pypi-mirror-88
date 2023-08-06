from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH>:HSDPa:DERRor:BIT:STATe \n
		The command activates bit error generation or deactivates it. Bit errors are inserted into the data stream of the coupled
		HS-PDSCHs. It is possible to select the layer in which the errors are inserted (physical or transport layer) . When the
		data source is read out, individual bits are deliberately inverted at random points in the data bit stream at the
		specified error rate in order to simulate an invalid signal. \n
			:param state: ON| OFF
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:HSDPa:DERRor:BIT:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH>:HSDPa:DERRor:BIT:STATe \n
		The command activates bit error generation or deactivates it. Bit errors are inserted into the data stream of the coupled
		HS-PDSCHs. It is possible to select the layer in which the errors are inserted (physical or transport layer) . When the
		data source is read out, individual bits are deliberately inverted at random points in the data bit stream at the
		specified error rate in order to simulate an invalid signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: state: ON| OFF"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:HSDPa:DERRor:BIT:STATe?')
		return Conversions.str_to_bool(response)
