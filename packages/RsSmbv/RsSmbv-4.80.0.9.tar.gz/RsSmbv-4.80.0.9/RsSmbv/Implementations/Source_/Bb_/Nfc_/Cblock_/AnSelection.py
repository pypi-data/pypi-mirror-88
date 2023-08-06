from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnSelection:
	"""AnSelection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("anSelection", core, parent)

	def set(self, anselection: enums.NfcAckNack, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:ANSelection \n
		Available only for 'PDU Type > ACK-NACK' or 'Block Type > R-block'. Selects ACK or NACK. \n
			:param anselection: ACK| NACK
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(anselection, enums.NfcAckNack)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:ANSelection {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcAckNack:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:ANSelection \n
		Available only for 'PDU Type > ACK-NACK' or 'Block Type > R-block'. Selects ACK or NACK. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: anselection: ACK| NACK"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:ANSelection?')
		return Conversions.str_to_scalar_enum(response, enums.NfcAckNack)
