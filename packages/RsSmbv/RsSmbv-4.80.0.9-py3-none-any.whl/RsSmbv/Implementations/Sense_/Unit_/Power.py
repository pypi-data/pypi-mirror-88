from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def set(self, power: enums.UnitPowSens, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:UNIT:[POWer] \n
		Selects the unit (Watt, dBm or dBμV) of measurement result display, queried with :​READ<ch>[:​POWer]?. \n
			:param power: DBM| DBUV| WATT
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.enum_scalar_to_str(power, enums.UnitPowSens)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:UNIT:POWer {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.UnitPowSens:
		"""SENSe<CH>:UNIT:[POWer] \n
		Selects the unit (Watt, dBm or dBμV) of measurement result display, queried with :​READ<ch>[:​POWer]?. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: power: DBM| DBUV| WATT"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:UNIT:POWer?')
		return Conversions.str_to_scalar_enum(response, enums.UnitPowSens)
