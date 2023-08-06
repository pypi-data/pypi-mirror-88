from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aperture:
	"""Aperture commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aperture", core, parent)

	def clone(self) -> 'Aperture':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Aperture(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def default(self):
		"""default commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_default'):
			from .Aperture_.Default import Default
			self._default = Default(self._core, self._base)
		return self._default

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Aperture_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time
