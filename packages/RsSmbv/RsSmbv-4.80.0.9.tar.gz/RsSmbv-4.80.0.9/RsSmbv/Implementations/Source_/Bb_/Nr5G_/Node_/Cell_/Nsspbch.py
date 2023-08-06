from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nsspbch:
	"""Nsspbch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nsspbch", core, parent)

	def set(self, nu_of_pbch_pattern: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:NSSPbch \n
		Sets the number of SS/PBCH patterns to be configured. \n
			:param nu_of_pbch_pattern: integer Range: 0 to 4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(nu_of_pbch_pattern)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:NSSPbch {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:NSSPbch \n
		Sets the number of SS/PBCH patterns to be configured. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: nu_of_pbch_pattern: integer Range: 0 to 4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:NSSPbch?')
		return Conversions.str_to_int(response)
