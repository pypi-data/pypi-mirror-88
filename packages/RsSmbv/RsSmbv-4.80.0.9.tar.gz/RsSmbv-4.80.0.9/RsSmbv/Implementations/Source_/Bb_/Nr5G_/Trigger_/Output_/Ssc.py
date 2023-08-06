from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssc:
	"""Ssc commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssc", core, parent)

	def clone(self) -> 'Ssc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ssc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ndlSymbols(self):
		"""ndlSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndlSymbols'):
			from .Ssc_.NdlSymbols import NdlSymbols
			self._ndlSymbols = NdlSymbols(self._core, self._base)
		return self._ndlSymbols

	@property
	def ngSymbols(self):
		"""ngSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ngSymbols'):
			from .Ssc_.NgSymbols import NgSymbols
			self._ngSymbols = NgSymbols(self._core, self._base)
		return self._ngSymbols

	@property
	def nulSymbols(self):
		"""nulSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nulSymbols'):
			from .Ssc_.NulSymbols import NulSymbols
			self._nulSymbols = NulSymbols(self._core, self._base)
		return self._nulSymbols

	@property
	def slfmt(self):
		"""slfmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slfmt'):
			from .Ssc_.Slfmt import Slfmt
			self._slfmt = Slfmt(self._core, self._base)
		return self._slfmt

	@property
	def ussIdx(self):
		"""ussIdx commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ussIdx'):
			from .Ssc_.UssIdx import UssIdx
			self._ussIdx = UssIdx(self._core, self._base)
		return self._ussIdx
