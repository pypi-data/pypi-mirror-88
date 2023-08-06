from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cqi:
	"""Cqi commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cqi", core, parent)

	def clone(self) -> 'Cqi':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cqi(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Cqi_.Bits import Bits
			self._bits = Bits(self._core, self._base)
		return self._bits

	@property
	def cbits(self):
		"""cbits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbits'):
			from .Cqi_.Cbits import Cbits
			self._cbits = Cbits(self._core, self._base)
		return self._cbits

	@property
	def codeword(self):
		"""codeword commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_codeword'):
			from .Cqi_.Codeword import Codeword
			self._codeword = Codeword(self._core, self._base)
		return self._codeword

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Cqi_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern
