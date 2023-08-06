from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Full:
	"""Full commands group definition. 10 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("full", core, parent)

	def clone(self) -> 'Full':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Full(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def area(self):
		"""area commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_area'):
			from .Full_.Area import Area
			self._area = Area(self._core, self._base)
		return self._area

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Full_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def rwindow(self):
		"""rwindow commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_rwindow'):
			from .Full_.Rwindow import Rwindow
			self._rwindow = Rwindow(self._core, self._base)
		return self._rwindow

	@property
	def scale(self):
		"""scale commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scale'):
			from .Full_.Scale import Scale
			self._scale = Scale(self._core, self._base)
		return self._scale
