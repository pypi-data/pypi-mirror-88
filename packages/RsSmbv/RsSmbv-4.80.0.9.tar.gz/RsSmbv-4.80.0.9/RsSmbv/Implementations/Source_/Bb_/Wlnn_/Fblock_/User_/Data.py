from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bpSymbol(self):
		"""bpSymbol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpSymbol'):
			from .Data_.BpSymbol import BpSymbol
			self._bpSymbol = BpSymbol(self._core, self._base)
		return self._bpSymbol

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Data_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Data_.Rate import Rate
			self._rate = Rate(self._core, self._base)
		return self._rate

	@property
	def symbols(self):
		"""symbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbols'):
			from .Data_.Symbols import Symbols
			self._symbols = Symbols(self._core, self._base)
		return self._symbols
