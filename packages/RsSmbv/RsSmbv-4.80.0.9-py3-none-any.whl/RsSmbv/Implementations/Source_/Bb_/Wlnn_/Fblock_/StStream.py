from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StStream:
	"""StStream commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stStream", core, parent)

	def set(self, ststream: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:STSTream \n
		Sets the number of the space time streams. This value depends on the number of spatial streams defined with command
		method RsSmbv.Source.Bb.Wlnn.Fblock.Sstream.set. Changing the number of the Spatial Streams immediately changes the value
		of the Space Time Streams to the same value. \n
			:param ststream: integer Range: 1 to dynamic
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.decimal_value_to_str(ststream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:STSTream {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:STSTream \n
		Sets the number of the space time streams. This value depends on the number of spatial streams defined with command
		method RsSmbv.Source.Bb.Wlnn.Fblock.Sstream.set. Changing the number of the Spatial Streams immediately changes the value
		of the Space Time Streams to the same value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ststream: integer Range: 1 to dynamic"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:STSTream?')
		return Conversions.str_to_int(response)
