from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trajectory:
	"""Trajectory commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trajectory", core, parent)

	def clone(self) -> 'Trajectory':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trajectory(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def svid(self):
		"""svid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svid'):
			from .Trajectory_.Svid import Svid
			self._svid = Svid(self._core, self._base)
		return self._svid

	@property
	def system(self):
		"""system commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_system'):
			from .Trajectory_.System import System
			self._system = System(self._core, self._base)
		return self._system
