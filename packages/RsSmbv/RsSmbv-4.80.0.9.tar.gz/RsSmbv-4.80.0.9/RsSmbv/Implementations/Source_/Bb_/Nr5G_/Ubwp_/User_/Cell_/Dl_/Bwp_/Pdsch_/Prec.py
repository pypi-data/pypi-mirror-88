from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prec:
	"""Prec commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prec", core, parent)

	def clone(self) -> 'Prec':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Prec(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bbSet1(self):
		"""bbSet1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbSet1'):
			from .Prec_.BbSet1 import BbSet1
			self._bbSet1 = BbSet1(self._core, self._base)
		return self._bbSet1

	@property
	def bsize(self):
		"""bsize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsize'):
			from .Prec_.Bsize import Bsize
			self._bsize = Bsize(self._core, self._base)
		return self._bsize

	@property
	def bsset2(self):
		"""bsset2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsset2'):
			from .Prec_.Bsset2 import Bsset2
			self._bsset2 = Bsset2(self._core, self._base)
		return self._bsset2

	@property
	def btype(self):
		"""btype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_btype'):
			from .Prec_.Btype import Btype
			self._btype = Btype(self._core, self._base)
		return self._btype

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Prec_.State import State
			self._state = State(self._core, self._base)
		return self._state
