from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhysBits:
	"""PhysBits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("physBits", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:PHYSbits \n
		Queries the allocation size in bits. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: physical_bits: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:PHYSbits?')
		return Conversions.str_to_int(response)
