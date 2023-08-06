from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adjust(self):
		"""adjust commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adjust'):
			from .Power_.Adjust import Adjust
			self._adjust = Adjust(self._core, self._base)
		return self._adjust

	def get_total(self) -> float:
		"""[SOURce<HW>]:BB:TDSCdma:POWer:[TOTal] \n
		Queries the total power of the active channels. After 'Power Adjust', this power corresponds to 0 dB. \n
			:return: total: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:POWer:TOTal?')
		return Conversions.str_to_float(response)
