from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inhibit:
	"""Inhibit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inhibit", core, parent)

	def set(self, inhibit: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:VOR:TRIGger:[EXTernal<CH>]:INHibit \n
		Specifies the duration by which a restart is inhibited. \n
			:param inhibit: integer Range: 0 to 67108863
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')"""
		param = Conversions.decimal_value_to_str(inhibit)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:TRIGger:EXTernal{channel_cmd_val}:INHibit {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:VOR:TRIGger:[EXTernal<CH>]:INHibit \n
		Specifies the duration by which a restart is inhibited. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')
			:return: inhibit: integer Range: 0 to 67108863"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:VOR:TRIGger:EXTernal{channel_cmd_val}:INHibit?')
		return Conversions.str_to_int(response)
