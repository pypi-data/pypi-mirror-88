from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scode:
	"""Scode commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scode", core, parent)

	def clone(self) -> 'Scode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Scode_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, scode: List[str], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:SCODe \n
		Sets the identification for the base station. This value is simultaneously the initial value of the scrambling code
		generator. \n
			:param scode: integer Range: #H0 to #H5FFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.list_to_csv_str(scode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:SCODe {param}')

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:SCODe \n
		Sets the identification for the base station. This value is simultaneously the initial value of the scrambling code
		generator. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: scode: integer Range: #H0 to #H5FFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:SCODe?')
		return Conversions.str_to_str_list(response)
