from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rdelay:
	"""Rdelay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdelay", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:EUTRa:TRIGger:EXTernal<CH>:RDELay \n
		Queries the time (in seconds) of an external trigger event is delayed for. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')
			:return: ext_result_delay: float Range: 0 to 688"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:EXTernal{channel_cmd_val}:RDELay?')
		return Conversions.str_to_float(response)
