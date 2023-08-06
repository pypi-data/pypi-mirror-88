from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nsize:
	"""Nsize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nsize", core, parent)

	def set(self, nfcid_1_sz: enums.NfcNfcid1Sz, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:NSIZe \n
		Determines the size of NFCID1. \n
			:param nfcid_1_sz: SINGle| DOUBle| TRIPle
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(nfcid_1_sz, enums.NfcNfcid1Sz)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NSIZe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcNfcid1Sz:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:NSIZe \n
		Determines the size of NFCID1. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: nfcid_1_sz: SINGle| DOUBle| TRIPle"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NSIZe?')
		return Conversions.str_to_scalar_enum(response, enums.NfcNfcid1Sz)
