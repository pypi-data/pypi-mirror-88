from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttime:
	"""Ttime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ttime", core, parent)

	def set(self, ttime: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TTIMe \n
		Sets the transition time when time domain windowing is active. The transition time defines the overlap range of two OFDM
		symbols. At a setting of 100 ns and if BW = 20 MHz, one sample overlaps. \n
			:param ttime: float Range: 0 to 1000 ns
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.decimal_value_to_str(ttime)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TTIMe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TTIMe \n
		Sets the transition time when time domain windowing is active. The transition time defines the overlap range of two OFDM
		symbols. At a setting of 100 ns and if BW = 20 MHz, one sample overlaps. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ttime: float Range: 0 to 1000 ns"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TTIMe?')
		return Conversions.str_to_float(response)
