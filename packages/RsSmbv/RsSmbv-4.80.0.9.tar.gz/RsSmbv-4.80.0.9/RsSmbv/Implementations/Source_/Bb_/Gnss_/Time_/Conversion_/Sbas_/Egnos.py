from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Egnos:
	"""Egnos commands group definition. 8 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("egnos", core, parent)

	def clone(self) -> 'Egnos':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Egnos(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def utc(self):
		"""utc commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_utc'):
			from .Egnos_.Utc import Utc
			self._utc = Utc(self._core, self._base)
		return self._utc
