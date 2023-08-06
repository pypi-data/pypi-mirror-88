from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ionospheric:
	"""Ionospheric commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ionospheric", core, parent)

	def clone(self) -> 'Ionospheric':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ionospheric(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alpha(self):
		"""alpha commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_alpha'):
			from .Ionospheric_.Alpha import Alpha
			self._alpha = Alpha(self._core, self._base)
		return self._alpha

	@property
	def beta(self):
		"""beta commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_beta'):
			from .Ionospheric_.Beta import Beta
			self._beta = Beta(self._core, self._base)
		return self._beta
