from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Velocity:
	"""Velocity commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("velocity", core, parent)

	def clone(self) -> 'Velocity':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Velocity(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ecef(self):
		"""ecef commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecef'):
			from .Velocity_.Ecef import Ecef
			self._ecef = Ecef(self._core, self._base)
		return self._ecef

	@property
	def lned(self):
		"""lned commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lned'):
			from .Velocity_.Lned import Lned
			self._lned = Lned(self._core, self._base)
		return self._lned
