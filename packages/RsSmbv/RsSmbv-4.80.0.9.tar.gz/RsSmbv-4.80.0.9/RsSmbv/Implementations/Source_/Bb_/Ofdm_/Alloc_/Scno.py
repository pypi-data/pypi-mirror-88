from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scno:
	"""Scno commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scno", core, parent)

	def set(self, no_of_subcarriers: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:SCNO \n
		Sets the number of allocated subcarriers. \n
			:param no_of_subcarriers: integer Range: 1 to 13107
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(no_of_subcarriers)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:SCNO {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:SCNO \n
		Sets the number of allocated subcarriers. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: no_of_subcarriers: integer Range: 1 to 13107"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:SCNO?')
		return Conversions.str_to_int(response)
