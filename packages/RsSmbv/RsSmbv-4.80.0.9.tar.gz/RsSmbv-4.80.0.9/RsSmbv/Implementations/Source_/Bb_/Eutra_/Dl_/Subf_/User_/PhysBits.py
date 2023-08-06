from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhysBits:
	"""PhysBits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("physBits", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:USER<CH>:PHYSbits \n
		Queries the size of the selected allocation in bits and considering the subcarriers that are used for other signals or
		channels with higher priority. If a User 1...4 is selected for the 'Data Source' in the allocation table for the
		corresponding allocation, the value of the parameter 'Number of Physical Bits' is the sum of the 'Physical Bits' of all
		single allocations that belong to the same user in the selected subframe. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: physical_bits: integer Range: 0 to 100000"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:USER{channel_cmd_val}:PHYSbits?')
		return Conversions.str_to_int(response)
