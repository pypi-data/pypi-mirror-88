from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ntps:
	"""Ntps commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ntps", core, parent)

	def set(self, ntps: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:NTPS \n
		(Available only for VHT Tx mode) Indicates whether VHT AP allows VHT non-AP STAs in TXOP power save mode to enter during
		TXOP. \n
			:param ntps: OFF| ON ON Indicates that the VHT AP allows VHT non-AP STAs to enter doze mode during a TXOP. OFF Indicates that the VHT AP does not allow VHT non-AP STAs to enter doze mode during a TXOP.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(ntps)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:NTPS {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:NTPS \n
		(Available only for VHT Tx mode) Indicates whether VHT AP allows VHT non-AP STAs in TXOP power save mode to enter during
		TXOP. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ntps: OFF| ON ON Indicates that the VHT AP allows VHT non-AP STAs to enter doze mode during a TXOP. OFF Indicates that the VHT AP does not allow VHT non-AP STAs to enter doze mode during a TXOP."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:NTPS?')
		return Conversions.str_to_bool(response)
