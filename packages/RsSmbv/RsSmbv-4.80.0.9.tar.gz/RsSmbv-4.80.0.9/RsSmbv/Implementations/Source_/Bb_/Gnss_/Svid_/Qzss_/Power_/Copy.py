from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Copy:
	"""Copy commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("copy", core, parent)

	def clone(self) -> 'Copy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Copy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Copy_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def svid(self):
		"""svid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svid'):
			from .Copy_.Svid import Svid
			self._svid = Svid(self._core, self._base)
		return self._svid
