from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duplexing:
	"""Duplexing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duplexing", core, parent)

	def set(self, dl_duplexmode: enums.EutraDuplexModeExtRange, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH>:DUPLexing \n
		Selects the duplexing mode of the component carriers. \n
			:param dl_duplexmode: TDD| FDD | LAA
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(dl_duplexmode, enums.EutraDuplexModeExtRange)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{channel_cmd_val}:DUPLexing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDuplexModeExtRange:
		"""[SOURce<HW>]:BB:EUTRa:DL:CA:CELL<CH>:DUPLexing \n
		Selects the duplexing mode of the component carriers. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: dl_duplexmode: TDD| FDD | LAA"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:CELL{channel_cmd_val}:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexModeExtRange)
