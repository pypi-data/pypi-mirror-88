from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nid2:
	"""Nid2 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nid2", core, parent)

	def set(self, nfcid_2: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:NID2 \n
		Determines the entire value of NFCID2. Is a virtual parameter for SCPI to set the NFCID2 either in NFC-DEP or Type 3 Tag
		mode. \n
			:param nfcid_2: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.list_to_csv_str(nfcid_2)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NID2 {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:NID2 \n
		Determines the entire value of NFCID2. Is a virtual parameter for SCPI to set the NFCID2 either in NFC-DEP or Type 3 Tag
		mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: nfcid_2: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NID2?')
		return Conversions.str_to_str_list(response)
