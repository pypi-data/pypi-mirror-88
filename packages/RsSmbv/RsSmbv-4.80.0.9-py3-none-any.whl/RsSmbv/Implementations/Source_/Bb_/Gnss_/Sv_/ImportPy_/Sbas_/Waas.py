from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Waas:
	"""Waas commands group definition. 6 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("waas", core, parent)

	def clone(self) -> 'Waas':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Waas(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def add(self):
		"""add commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_add'):
			from .Waas_.Add import Add
			self._add = Add(self._core, self._base)
		return self._add

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Waas_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .Waas_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def remove(self):
		"""remove commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_remove'):
			from .Waas_.Remove import Remove
			self._remove = Remove(self._core, self._base)
		return self._remove
