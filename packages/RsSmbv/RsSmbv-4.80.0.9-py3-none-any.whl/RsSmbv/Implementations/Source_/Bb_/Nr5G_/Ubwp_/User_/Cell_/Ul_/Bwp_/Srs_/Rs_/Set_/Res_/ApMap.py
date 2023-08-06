from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApMap:
	"""ApMap commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apMap", core, parent)

	def clone(self) -> 'ApMap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApMap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ap3000(self):
		"""ap3000 commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap3000'):
			from .ApMap_.Ap3000 import Ap3000
			self._ap3000 = Ap3000(self._core, self._base)
		return self._ap3000
