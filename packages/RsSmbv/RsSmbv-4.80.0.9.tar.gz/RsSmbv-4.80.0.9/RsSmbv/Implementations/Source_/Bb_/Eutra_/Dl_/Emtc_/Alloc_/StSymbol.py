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

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NumberA:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:STSYmbol \n
		Queries the first symbol where the channel can be allocated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: start_symbol: 1| 2| 3| 4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:STSYmbol?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)
