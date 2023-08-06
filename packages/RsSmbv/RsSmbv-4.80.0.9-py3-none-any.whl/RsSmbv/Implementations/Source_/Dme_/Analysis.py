from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Analysis:
	"""Analysis commands group definition. 9 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("analysis", core, parent)

	def clone(self) -> 'Analysis':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Analysis(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def efficiency(self):
		"""efficiency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_efficiency'):
			from .Analysis_.Efficiency import Efficiency
			self._efficiency = Efficiency(self._core, self._base)
		return self._efficiency

	@property
	def gate(self):
		"""gate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gate'):
			from .Analysis_.Gate import Gate
			self._gate = Gate(self._core, self._base)
		return self._gate

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Analysis_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def prRate(self):
		"""prRate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_prRate'):
			from .Analysis_.PrRate import PrRate
			self._prRate = PrRate(self._core, self._base)
		return self._prRate

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_time'):
			from .Analysis_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time
