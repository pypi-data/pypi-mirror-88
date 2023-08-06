from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DptListen:
	"""DptListen commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dptListen", core, parent)

	def set(self, dptl: enums.NfcDivisor, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:DPTListen \n
		In ATTRIB command, sets the divisor in the corresponding transmission direction. \n
			:param dptl: DIV1| DIV2| DIV4| DIV8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(dptl, enums.NfcDivisor)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DPTListen {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcDivisor:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:DPTListen \n
		In ATTRIB command, sets the divisor in the corresponding transmission direction. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: dptl: DIV1| DIV2| DIV4| DIV8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DPTListen?')
		return Conversions.str_to_scalar_enum(response, enums.NfcDivisor)
