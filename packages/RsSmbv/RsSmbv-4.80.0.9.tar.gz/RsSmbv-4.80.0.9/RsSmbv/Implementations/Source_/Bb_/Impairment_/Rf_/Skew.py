from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Skew:
	"""Skew commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("skew", core, parent)

	def set(self, skew: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:BB:IMPairment:RF<CH>:SKEW \n
		Sets a delay between the Q vector and the I vector of the corresponding stream. \n
			:param skew: float Range: -500E-9 to 500E-9
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(skew)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:SKEW {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:BB:IMPairment:RF<CH>:SKEW \n
		Sets a delay between the Q vector and the I vector of the corresponding stream. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: skew: float Range: -500E-9 to 500E-9"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:SKEW?')
		return Conversions.str_to_float(response)
