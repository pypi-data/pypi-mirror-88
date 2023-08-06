from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aattributes:
	"""Aattributes commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aattributes", core, parent)

	def set(self, aattributes: enums.NfcAcssAttrib, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SERVice<ST>:AATTributes \n
		Enables the Service Code List Configuration. \n
			:param aattributes: AARW| AARO
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Service')"""
		param = Conversions.enum_scalar_to_str(aattributes, enums.NfcAcssAttrib)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SERVice{stream_cmd_val}:AATTributes {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.NfcAcssAttrib:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SERVice<ST>:AATTributes \n
		Enables the Service Code List Configuration. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Service')
			:return: aattributes: AARW| AARO"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SERVice{stream_cmd_val}:AATTributes?')
		return Conversions.str_to_scalar_enum(response, enums.NfcAcssAttrib)
