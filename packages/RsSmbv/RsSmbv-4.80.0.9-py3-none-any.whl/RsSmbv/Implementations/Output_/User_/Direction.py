from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Direction:
	"""Direction commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("direction", core, parent)

	def set(self, direction: enums.ConnDirection, channel=repcap.Channel.Default) -> None:
		"""OUTPut<HW>:USER<CH>:DIRection \n
		Determines whether the connector is used as an input or an output. \n
			:param direction: INPut| OUTPut| UNUSed UNUSed = the connector is not defined
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(direction, enums.ConnDirection)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'OUTPut<HwInstance>:USER{channel_cmd_val}:DIRection {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.ConnDirection:
		"""OUTPut<HW>:USER<CH>:DIRection \n
		Determines whether the connector is used as an input or an output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: direction: INPut| OUTPut| UNUSed UNUSed = the connector is not defined"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'OUTPut<HwInstance>:USER{channel_cmd_val}:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.ConnDirection)
