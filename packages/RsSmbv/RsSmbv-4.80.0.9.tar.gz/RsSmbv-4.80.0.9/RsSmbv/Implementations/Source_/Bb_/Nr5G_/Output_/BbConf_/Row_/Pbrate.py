from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pbrate:
	"""Pbrate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pbrate", core, parent)

	def set(self, playback_rate: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:BBConf:ROW<CH>:PBRate \n
		For method RsSmbv.Source.Bb.Nr5G.Output.BbConf.Row.Variation.set 1, sets the playback speed. \n
			:param playback_rate: integer Per default, the playback rate is the same as the calculated sample rate but the value range also depends on the installed options. Range: 0 to 24e8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(playback_rate)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:BBConf:ROW{channel_cmd_val}:PBRate {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:BBConf:ROW<CH>:PBRate \n
		For method RsSmbv.Source.Bb.Nr5G.Output.BbConf.Row.Variation.set 1, sets the playback speed. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: playback_rate: integer Per default, the playback rate is the same as the calculated sample rate but the value range also depends on the installed options. Range: 0 to 24e8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:OUTPut:BBConf:ROW{channel_cmd_val}:PBRate?')
		return Conversions.str_to_int(response)
