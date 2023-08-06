from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cs:
	"""Cs commands group definition. 206 total commands, 10 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cs", core, parent)

	def clone(self) -> 'Cs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aulBwp(self):
		"""aulBwp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aulBwp'):
			from .Cs_.AulBwp import AulBwp
			self._aulBwp = AulBwp(self._core, self._base)
		return self._aulBwp

	@property
	def dcces(self):
		"""dcces commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcces'):
			from .Cs_.Dcces import Dcces
			self._dcces = Dcces(self._core, self._base)
		return self._dcces

	@property
	def dci(self):
		"""dci commands group. 183 Sub-classes, 0 commands."""
		if not hasattr(self, '_dci'):
			from .Cs_.Dci import Dci
			self._dci = Dci(self._core, self._base)
		return self._dci

	@property
	def dmrs(self):
		"""dmrs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Cs_.Dmrs import Dmrs
			self._dmrs = Dmrs(self._core, self._base)
		return self._dmrs

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Cs_.Id import Id
			self._id = Id(self._core, self._base)
		return self._id

	@property
	def il(self):
		"""il commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_il'):
			from .Cs_.Il import Il
			self._il = Il(self._core, self._base)
		return self._il

	@property
	def ndci(self):
		"""ndci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndci'):
			from .Cs_.Ndci import Ndci
			self._ndci = Ndci(self._core, self._base)
		return self._ndci

	@property
	def preGran(self):
		"""preGran commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preGran'):
			from .Cs_.PreGran import PreGran
			self._preGran = PreGran(self._core, self._base)
		return self._preGran

	@property
	def resAlloc(self):
		"""resAlloc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_resAlloc'):
			from .Cs_.ResAlloc import ResAlloc
			self._resAlloc = ResAlloc(self._core, self._base)
		return self._resAlloc

	@property
	def tci(self):
		"""tci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tci'):
			from .Cs_.Tci import Tci
			self._tci = Tci(self._core, self._base)
		return self._tci
