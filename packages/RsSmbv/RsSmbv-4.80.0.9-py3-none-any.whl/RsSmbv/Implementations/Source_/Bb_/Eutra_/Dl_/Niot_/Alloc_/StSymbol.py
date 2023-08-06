from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StSymbol:
	"""StSymbol commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stSymbol", core, parent)

	def set(self, start_symbol: enums.EutraDlNbiotStartSymbols, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:ALLoc<CH>:STSYmbol \n
		Sets the first symbol in a subframe where NB-IoT channels can be allocated. \n
			:param start_symbol: SYM0| SYM1| SYM2| SYM3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(start_symbol, enums.EutraDlNbiotStartSymbols)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:ALLoc{channel_cmd_val}:STSYmbol {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDlNbiotStartSymbols:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:ALLoc<CH>:STSYmbol \n
		Sets the first symbol in a subframe where NB-IoT channels can be allocated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: start_symbol: SYM0| SYM1| SYM2| SYM3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:ALLoc{channel_cmd_val}:STSYmbol?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDlNbiotStartSymbols)
