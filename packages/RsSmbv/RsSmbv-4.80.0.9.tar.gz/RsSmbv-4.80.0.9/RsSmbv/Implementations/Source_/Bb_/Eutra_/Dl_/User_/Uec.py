from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uec:
	"""Uec commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uec", core, parent)

	def set(self, ue_category: enums.EutraUeCat, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:UEC \n
		Sets the UE Category. \n
			:param ue_category: USER | C1| C2| C3| C4| C5| C6| C7| C8| C9| C10| C11| C12| C13| C14| C15| C16| C17| C18| C19| C20 | M1| NB1 | M2| NB2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(ue_category, enums.EutraUeCat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:UEC {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraUeCat:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:UEC \n
		Sets the UE Category. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: ue_category: USER | C1| C2| C3| C4| C5| C6| C7| C8| C9| C10| C11| C12| C13| C14| C15| C16| C17| C18| C19| C20 | M1| NB1 | M2| NB2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:UEC?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUeCat)
