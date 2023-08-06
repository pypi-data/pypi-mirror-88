from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lreduction:
	"""Lreduction commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lreduction", core, parent)

	def set(self, lreduction: enums.NfcLenReduct, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:LREDuction \n
		Selects the length reduction (LR) . \n
			:param lreduction: LR64| LR128| LR192| LR254
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(lreduction, enums.NfcLenReduct)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:LREDuction {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcLenReduct:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:LREDuction \n
		Selects the length reduction (LR) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: lreduction: LR64| LR128| LR192| LR254"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:LREDuction?')
		return Conversions.str_to_scalar_enum(response, enums.NfcLenReduct)
