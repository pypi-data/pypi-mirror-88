from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icomponent:
	"""Icomponent commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icomponent", core, parent)

	def set(self, ipart: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:BB:IMPairment:RF<CH>:LEAKage:I \n
		Determines the leakage amplitude of the I or Q signal component of the corresponding stream \n
			:param ipart: float Range: -10 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(ipart)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:LEAKage:I {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:BB:IMPairment:RF<CH>:LEAKage:I \n
		Determines the leakage amplitude of the I or Q signal component of the corresponding stream \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: ipart: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:LEAKage:I?')
		return Conversions.str_to_float(response)
