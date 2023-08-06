from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Used:
	"""Used commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("used", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:CHANnels:USED \n
		Queries the number of active channels. The maximum number of active channels depends on the installed options, see
		'Channel Budget'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: used_channels: integer Range: 0 to depends on installed options The *RST value depends on the installed GNSS system option, e.g. for GPS : *RST: 11"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:CHANnels:USED?')
		return Conversions.str_to_int(response)
