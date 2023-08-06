from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpcch:
	"""Dpcch commands group definition. 13 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpcch", core, parent)

	def clone(self) -> 'Dpcch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpcch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mcode(self):
		"""mcode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcode'):
			from .Dpcch_.Mcode import Mcode
			self._mcode = Mcode(self._core, self._base)
		return self._mcode

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plength'):
			from .Dpcch_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	@property
	def poffset(self):
		"""poffset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_poffset'):
			from .Dpcch_.Poffset import Poffset
			self._poffset = Poffset(self._core, self._base)
		return self._poffset

	@property
	def tfci(self):
		"""tfci commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Dpcch_.Tfci import Tfci
			self._tfci = Tfci(self._core, self._base)
		return self._tfci

	@property
	def tpc(self):
		"""tpc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Dpcch_.Tpc import Tpc
			self._tpc = Tpc(self._core, self._base)
		return self._tpc
