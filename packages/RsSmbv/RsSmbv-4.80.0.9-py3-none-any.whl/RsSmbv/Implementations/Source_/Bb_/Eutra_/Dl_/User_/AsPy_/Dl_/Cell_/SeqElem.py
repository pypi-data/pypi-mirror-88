from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqElem:
	"""SeqElem commands group definition. 12 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("seqElem", core, parent)

	def clone(self) -> 'SeqElem':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeqElem(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .SeqElem_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def harq(self):
		"""harq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harq'):
			from .SeqElem_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def pdre(self):
		"""pdre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdre'):
			from .SeqElem_.Pdre import Pdre
			self._pdre = Pdre(self._core, self._base)
		return self._pdre

	@property
	def subframe(self):
		"""subframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subframe'):
			from .SeqElem_.Subframe import Subframe
			self._subframe = Subframe(self._core, self._base)
		return self._subframe

	@property
	def tb1(self):
		"""tb1 commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb1'):
			from .SeqElem_.Tb1 import Tb1
			self._tb1 = Tb1(self._core, self._base)
		return self._tb1

	@property
	def tb2(self):
		"""tb2 commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb2'):
			from .SeqElem_.Tb2 import Tb2
			self._tb2 = Tb2(self._core, self._base)
		return self._tb2
