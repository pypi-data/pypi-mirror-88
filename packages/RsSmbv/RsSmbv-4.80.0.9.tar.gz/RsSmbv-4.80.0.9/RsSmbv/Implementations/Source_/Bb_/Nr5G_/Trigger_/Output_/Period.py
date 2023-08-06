from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Period:
	"""Period commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("period", core, parent)

	def set(self, mark_usr_per: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:PERiod \n
		Sets the period of the user-defined period marker. \n
			:param mark_usr_per: integer Range: 1 to 4294967295
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(mark_usr_per)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:PERiod {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:PERiod \n
		Sets the period of the user-defined period marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mark_usr_per: integer Range: 1 to 4294967295"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:PERiod?')
		return Conversions.str_to_int(response)
