from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Speriod:
	"""Speriod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("speriod", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TIMing:SPERiod \n
		Queries the structure length. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: sp_eriod: float"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:TIMing:SPERiod?')
		return Conversions.str_to_float(response)
