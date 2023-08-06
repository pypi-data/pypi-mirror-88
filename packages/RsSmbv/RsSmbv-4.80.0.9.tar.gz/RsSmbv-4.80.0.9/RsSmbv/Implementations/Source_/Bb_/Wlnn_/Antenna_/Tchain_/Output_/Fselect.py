from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fselect:
	"""Fselect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fselect", core, parent)

	def set(self, fselect: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:ANTenna:TCHain<CH>:OUTPut:FSELect \n
		The command saves the IQ chain in a file. \n
			:param fselect: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tchain')"""
		param = Conversions.value_to_quoted_str(fselect)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:ANTenna:TCHain{channel_cmd_val}:OUTPut:FSELect {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:WLNN:ANTenna:TCHain<CH>:OUTPut:FSELect \n
		The command saves the IQ chain in a file. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tchain')
			:return: fselect: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:ANTenna:TCHain{channel_cmd_val}:OUTPut:FSELect?')
		return trim_str_response(response)
