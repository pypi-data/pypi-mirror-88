from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	def set(self, deviation: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:DM:FSK:VARiable:SYMBol<CH>:DEViation \n
		Sets the deviation of the selected symbol for variable FSK modulation mode. \n
			:param deviation: float The value range depends on the selected symbol rate (see data sheet) . Range: -40E6 to 40E6, Unit: Hz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Symbol')"""
		param = Conversions.decimal_value_to_str(deviation)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FSK:VARiable:SYMBol{channel_cmd_val}:DEViation {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:DM:FSK:VARiable:SYMBol<CH>:DEViation \n
		Sets the deviation of the selected symbol for variable FSK modulation mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Symbol')
			:return: deviation: float The value range depends on the selected symbol rate (see data sheet) . Range: -40E6 to 40E6, Unit: Hz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DM:FSK:VARiable:SYMBol{channel_cmd_val}:DEViation?')
		return Conversions.str_to_float(response)
