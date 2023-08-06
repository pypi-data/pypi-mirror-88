from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Depth:
	"""Depth commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("depth", core, parent)

	def get_sum(self) -> float:
		"""[SOURce<HW>]:AM:DEPTh:SUM \n
		Sets the total depth of the LF signal when using combined signal sources in amplitude modulation. \n
			:return: am_depth_sum: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AM:DEPTh:SUM?')
		return Conversions.str_to_float(response)

	def set_sum(self, am_depth_sum: float) -> None:
		"""[SOURce<HW>]:AM:DEPTh:SUM \n
		Sets the total depth of the LF signal when using combined signal sources in amplitude modulation. \n
			:param am_depth_sum: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(am_depth_sum)
		self._core.io.write(f'SOURce<HwInstance>:AM:DEPTh:SUM {param}')

	def set(self, depth: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:AM<CH>:[DEPTh] \n
		Sets the depth of the amplitude modulation in percent. \n
			:param depth: float Range: 0 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')"""
		param = Conversions.decimal_value_to_str(depth)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AM{channel_cmd_val}:DEPTh {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:AM<CH>:[DEPTh] \n
		Sets the depth of the amplitude modulation in percent. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: depth: float Range: 0 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{channel_cmd_val}:DEPTh?')
		return Conversions.str_to_float(response)
