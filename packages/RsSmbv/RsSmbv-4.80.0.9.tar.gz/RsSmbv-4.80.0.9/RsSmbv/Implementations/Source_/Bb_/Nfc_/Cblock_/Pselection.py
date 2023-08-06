from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pselection:
	"""Pselection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pselection", core, parent)

	def set(self, pselection: enums.NfcPcktSelect, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:PSELection \n
		Selects if the first or second packet of the SECTOR_SELECT command is transmitted. \n
			:param pselection: PCK1| PCK2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(pselection, enums.NfcPcktSelect)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:PSELection {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcPcktSelect:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:PSELection \n
		Selects if the first or second packet of the SECTOR_SELECT command is transmitted. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: pselection: PCK1| PCK2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:PSELection?')
		return Conversions.str_to_scalar_enum(response, enums.NfcPcktSelect)
