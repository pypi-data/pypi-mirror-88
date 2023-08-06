from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Snumber:
	"""Snumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("snumber", core, parent)

	def set(self, snumber: enums.NfcSlotNumber, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SNUMber \n
		Determines the slot number. \n
			:param snumber: SN2| SN3| SN4| SN5| SN6| SN7| SN8| SN9| SN10| SN11| SN12| SN13| SN14| SN15| SN16
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(snumber, enums.NfcSlotNumber)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SNUMber {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcSlotNumber:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SNUMber \n
		Determines the slot number. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: snumber: SN2| SN3| SN4| SN5| SN6| SN7| SN8| SN9| SN10| SN11| SN12| SN13| SN14| SN15| SN16"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SNUMber?')
		return Conversions.str_to_scalar_enum(response, enums.NfcSlotNumber)
