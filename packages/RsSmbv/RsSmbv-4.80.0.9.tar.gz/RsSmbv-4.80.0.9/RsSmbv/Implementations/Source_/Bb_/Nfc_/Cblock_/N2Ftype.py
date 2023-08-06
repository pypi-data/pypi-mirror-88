from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N2Ftype:
	"""N2Ftype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("n2Ftype", core, parent)

	def set(self, nf_type: enums.NfcNfcid2FmtTp, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:N2FType \n
		Determines which protocol or platform the NFCID2 format is for. \n
			:param nf_type: NDEP| TT3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(nf_type, enums.NfcNfcid2FmtTp)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:N2FType {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcNfcid2FmtTp:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:N2FType \n
		Determines which protocol or platform the NFCID2 format is for. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: nf_type: NDEP| TT3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:N2FType?')
		return Conversions.str_to_scalar_enum(response, enums.NfcNfcid2FmtTp)
