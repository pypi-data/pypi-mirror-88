from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmodel:
	"""Tmodel commands group definition. 10 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmodel", core, parent)

	def clone(self) -> 'Tmodel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tmodel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dl(self):
		"""dl commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dl'):
			from .Tmodel_.Dl import Dl
			self._dl = Dl(self._core, self._base)
		return self._dl

	@property
	def filterPy(self):
		"""filterPy commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_filterPy'):
			from .Tmodel_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def ul(self):
		"""ul commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ul'):
			from .Tmodel_.Ul import Ul
			self._ul = Ul(self._core, self._base)
		return self._ul
