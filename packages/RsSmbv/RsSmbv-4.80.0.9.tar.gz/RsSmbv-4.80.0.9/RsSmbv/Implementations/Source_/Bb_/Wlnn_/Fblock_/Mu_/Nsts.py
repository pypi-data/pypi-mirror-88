from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nsts:
	"""Nsts commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nsts", core, parent)

	def set(self, no_of_sts: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MU<ST>:NSTS \n
		Sets the number of space time streams for each user. \n
			:param no_of_sts: integer Range: 0 to Max
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mu')"""
		param = Conversions.decimal_value_to_str(no_of_sts)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MU{stream_cmd_val}:NSTS {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MU<ST>:NSTS \n
		Sets the number of space time streams for each user. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mu')
			:return: no_of_sts: integer Range: 0 to Max"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MU{stream_cmd_val}:NSTS?')
		return Conversions.str_to_int(response)
