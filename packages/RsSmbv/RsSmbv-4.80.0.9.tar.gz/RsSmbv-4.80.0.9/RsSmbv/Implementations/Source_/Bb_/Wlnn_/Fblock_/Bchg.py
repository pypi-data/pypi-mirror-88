from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bchg:
	"""Bchg commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bchg", core, parent)

	def set(self, beam_change: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:BCHG \n
		If enabled, the beam is changed between pre-HE and HE modulated fields. \n
			:param beam_change: OFF| ON| 1| 0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(beam_change)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BCHG {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:BCHG \n
		If enabled, the beam is changed between pre-HE and HE modulated fields. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: beam_change: OFF| ON| 1| 0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BCHG?')
		return Conversions.str_to_bool(response)
