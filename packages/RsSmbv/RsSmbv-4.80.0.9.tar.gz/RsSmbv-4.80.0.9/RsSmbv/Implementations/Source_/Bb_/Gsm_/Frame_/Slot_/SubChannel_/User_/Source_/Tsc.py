from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tsc:
	"""Tsc commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tsc", core, parent)

	def clone(self) -> 'Tsc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tsc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Tsc_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Tsc_.Set import Set
			self._set = Set(self._core, self._base)
		return self._set

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Tsc_.User import User
			self._user = User(self._core, self._base)
		return self._user
