from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Smoothing:
	"""Smoothing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("smoothing", core, parent)

	def set(self, smoothing: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMOothing \n
		(available for all Tx modes, except VHT) This command indicates to the receiver whether frequency-domain smoothing is
		recommended as part of channel estimation. \n
			:param smoothing: OFF| ON ON Indicates that channel estimate smoothing is recommended. OFF Indicates that only per-carrier independent channel (unsmoothed) estimate is recommended.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(smoothing)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMOothing {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMOothing \n
		(available for all Tx modes, except VHT) This command indicates to the receiver whether frequency-domain smoothing is
		recommended as part of channel estimation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: smoothing: OFF| ON ON Indicates that channel estimate smoothing is recommended. OFF Indicates that only per-carrier independent channel (unsmoothed) estimate is recommended."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMOothing?')
		return Conversions.str_to_bool(response)
