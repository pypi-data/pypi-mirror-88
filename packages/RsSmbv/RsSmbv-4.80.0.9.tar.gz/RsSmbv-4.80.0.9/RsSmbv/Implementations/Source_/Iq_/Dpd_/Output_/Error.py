from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Error:
	"""Error commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("error", core, parent)

	def clone(self) -> 'Error':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Error(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def max(self):
		"""max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_max'):
			from .Error_.Max import Max
			self._max = Max(self._core, self._base)
		return self._max

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:IQ:DPD<ST>:OUTPut:ERRor \n
		Queries the resulting level error. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: achieved_error: float"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:OUTPut:ERRor?')
		return Conversions.str_to_float(response)
