from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Avrl:
	"""Avrl commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("avrl", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:POWer:BBConf:ROW<CH>:AVRL \n
		Queries the available basebands with their average power. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: pow_per_bb_rel_lvl: float Range: -80 to 10"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:BBConf:ROW{channel_cmd_val}:AVRL?')
		return Conversions.str_to_float(response)
