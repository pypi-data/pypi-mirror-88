from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sensitivity:
	"""Sensitivity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sensitivity", core, parent)

	def set(self, sensitivity: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:AM<CH>:SENSitivity \n
		Sets the sensitivity of the external signal source for amplitude modulation in %/V. \n
			:param sensitivity: float Range: 0 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')"""
		param = Conversions.decimal_value_to_str(sensitivity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AM{channel_cmd_val}:SENSitivity {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:AM<CH>:SENSitivity \n
		Sets the sensitivity of the external signal source for amplitude modulation in %/V. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: sensitivity: float Range: 0 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{channel_cmd_val}:SENSitivity?')
		return Conversions.str_to_float(response)
