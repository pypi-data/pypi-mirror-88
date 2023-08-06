from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Codebook:
	"""Codebook commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("codebook", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:SCMA:CODebook \n
		Queries the codebook size. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: codebook: integer Range: 0 to 4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:SCMA:CODebook?')
		return Conversions.str_to_int(response)
