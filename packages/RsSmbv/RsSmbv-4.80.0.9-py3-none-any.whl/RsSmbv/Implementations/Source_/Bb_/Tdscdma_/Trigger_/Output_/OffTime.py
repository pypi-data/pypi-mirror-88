from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffTime:
	"""OffTime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offTime", core, parent)

	def set(self, off_time: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:TRIGger:OUTPut<CH>:OFFTime \n
		Sets the number of chips during which the marker output is on or off. \n
			:param off_time: integer Range: 1 to 16777215
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(off_time)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:TRIGger:OUTPut{channel_cmd_val}:OFFTime {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:TRIGger:OUTPut<CH>:OFFTime \n
		Sets the number of chips during which the marker output is on or off. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: off_time: integer Range: 1 to 16777215"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:TRIGger:OUTPut{channel_cmd_val}:OFFTime?')
		return Conversions.str_to_int(response)
