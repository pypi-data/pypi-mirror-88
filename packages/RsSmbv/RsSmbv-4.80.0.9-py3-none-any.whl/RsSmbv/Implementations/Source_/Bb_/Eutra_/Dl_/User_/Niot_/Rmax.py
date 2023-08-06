from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rmax:
	"""Rmax commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmax", core, parent)

	def set(self, max_rep_npdcch: enums.EutraNbiotRmAx, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:NIOT:RMAX \n
		Sets the maximum number NPDCCH is repeated RMax. \n
			:param max_rep_npdcch: R1| R2| R4| R8| R16| R32| R64| R128| R256| R512| R1024| R2048
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(max_rep_npdcch, enums.EutraNbiotRmAx)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:NIOT:RMAX {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraNbiotRmAx:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:NIOT:RMAX \n
		Sets the maximum number NPDCCH is repeated RMax. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: max_rep_npdcch: R1| R2| R4| R8| R16| R32| R64| R128| R256| R512| R1024| R2048"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:NIOT:RMAX?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotRmAx)
