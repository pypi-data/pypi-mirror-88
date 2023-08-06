from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tbs:
	"""Tbs commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbs", core, parent)

	def clone(self) -> 'Tbs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tbs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Tbs_.Index import Index
			self._index = Index(self._core, self._base)
		return self._index

	@property
	def table(self):
		"""table commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_table'):
			from .Tbs_.Table import Table
			self._table = Table(self._core, self._base)
		return self._table
