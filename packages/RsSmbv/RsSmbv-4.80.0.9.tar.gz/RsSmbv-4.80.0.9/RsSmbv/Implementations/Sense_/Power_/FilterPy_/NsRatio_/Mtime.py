from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mtime:
	"""Mtime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mtime", core, parent)

	def set(self, mtime: float, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:FILTer:NSRatio:MTIMe \n
		Sets an upper limit for the settling time of the auto-averaging filter in the NSRatio mode and thus limits the length of
		the filter. The filter type is set with command FILTer:TYPE. \n
			:param mtime: float Range: 1 to 999.99
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.decimal_value_to_str(mtime)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:FILTer:NSRatio:MTIMe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SENSe<CH>:[POWer]:FILTer:NSRatio:MTIMe \n
		Sets an upper limit for the settling time of the auto-averaging filter in the NSRatio mode and thus limits the length of
		the filter. The filter type is set with command FILTer:TYPE. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: mtime: float Range: 1 to 999.99"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:FILTer:NSRatio:MTIMe?')
		return Conversions.str_to_float(response)
