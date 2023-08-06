from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpcch:
	"""Dpcch commands group definition. 60 total commands, 8 Sub-groups, 0 group commands"""

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
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Dpcch_.Ccode import Ccode
			self._ccode = Ccode(self._core, self._base)
		return self._ccode

	@property
	def fbi(self):
		"""fbi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fbi'):
			from .Dpcch_.Fbi import Fbi
			self._fbi = Fbi(self._core, self._base)
		return self._fbi

	@property
	def hs(self):
		"""hs commands group. 20 Sub-classes, 0 commands."""
		if not hasattr(self, '_hs'):
			from .Dpcch_.Hs import Hs
			self._hs = Hs(self._core, self._base)
		return self._hs

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Dpcch_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Dpcch_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def tfci(self):
		"""tfci commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Dpcch_.Tfci import Tfci
			self._tfci = Tfci(self._core, self._base)
		return self._tfci

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Dpcch_.Toffset import Toffset
			self._toffset = Toffset(self._core, self._base)
		return self._toffset

	@property
	def tpc(self):
		"""tpc commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Dpcch_.Tpc import Tpc
			self._tpc = Tpc(self._core, self._base)
		return self._tpc
