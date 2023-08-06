from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scmd:
	"""Scmd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scmd", core, parent)

	def set(self, scmd: enums.NfcSelCmd, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SCMD \n
		Selects the cascade level (CL) of the NFCID1 requested by the NFC Forum Device in Poll Mode. \n
			:param scmd: CL1| CL2| CL3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(scmd, enums.NfcSelCmd)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SCMD {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcSelCmd:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SCMD \n
		Selects the cascade level (CL) of the NFCID1 requested by the NFC Forum Device in Poll Mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: scmd: CL1| CL2| CL3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SCMD?')
		return Conversions.str_to_scalar_enum(response, enums.NfcSelCmd)
