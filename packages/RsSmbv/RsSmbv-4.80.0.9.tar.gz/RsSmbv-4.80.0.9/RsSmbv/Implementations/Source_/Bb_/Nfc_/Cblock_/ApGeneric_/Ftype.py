from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ftype:
	"""Ftype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ftype", core, parent)

	def set(self, frame_type: enums.NfcApgEnericFrameType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:FTYPe \n
		Selects a frame type for 'Command Type > GENERIC'. \n
			:param frame_type: SHORt| STANdard| BOSDd
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(frame_type, enums.NfcApgEnericFrameType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:APGeneric:FTYPe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcApgEnericFrameType:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:FTYPe \n
		Selects a frame type for 'Command Type > GENERIC'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: frame_type: SHORt| STANdard| BOSDd"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:APGeneric:FTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.NfcApgEnericFrameType)
