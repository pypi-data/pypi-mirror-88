from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Imask:
	"""Imask commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("imask", core, parent)

	def set(self, imask: List[str], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:IMASk \n
		Sets the long code mask of the I channel. \n
			:param imask: 44 bits
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.list_to_csv_str(imask)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:IMASk {param}')

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:IMASk \n
		Sets the long code mask of the I channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: imask: 44 bits"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:IMASk?')
		return Conversions.str_to_str_list(response)
