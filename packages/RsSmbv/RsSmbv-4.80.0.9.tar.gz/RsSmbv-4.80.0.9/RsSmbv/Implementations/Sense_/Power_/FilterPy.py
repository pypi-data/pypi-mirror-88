from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 6 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def length(self):
		"""length commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_length'):
			from .FilterPy_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def nsRatio(self):
		"""nsRatio commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsRatio'):
			from .FilterPy_.NsRatio import NsRatio
			self._nsRatio = NsRatio(self._core, self._base)
		return self._nsRatio

	@property
	def sonce(self):
		"""sonce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sonce'):
			from .FilterPy_.Sonce import Sonce
			self._sonce = Sonce(self._core, self._base)
		return self._sonce

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .FilterPy_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
