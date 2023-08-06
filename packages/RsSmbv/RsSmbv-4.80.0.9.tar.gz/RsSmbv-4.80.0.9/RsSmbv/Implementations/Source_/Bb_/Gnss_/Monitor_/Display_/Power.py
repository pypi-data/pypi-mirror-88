from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 24 total commands, 2 Sub-groups, 0 group commands"""

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
	def echoes(self):
		"""echoes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_echoes'):
			from .Power_.Echoes import Echoes
			self._echoes = Echoes(self._core, self._base)
		return self._echoes

	@property
	def system(self):
		"""system commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_system'):
			from .Power_.System import System
			self._system = System(self._core, self._base)
		return self._system
