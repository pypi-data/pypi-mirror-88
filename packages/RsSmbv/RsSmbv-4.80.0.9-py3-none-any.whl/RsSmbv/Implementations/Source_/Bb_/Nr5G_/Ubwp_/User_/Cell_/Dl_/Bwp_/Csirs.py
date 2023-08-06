from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csirs:
	"""Csirs commands group definition. 44 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csirs", core, parent)

	def clone(self) -> 'Csirs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Csirs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def azp(self):
		"""azp commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_azp'):
			from .Csirs_.Azp import Azp
			self._azp = Azp(self._core, self._base)
		return self._azp

	@property
	def nzp(self):
		"""nzp commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_nzp'):
			from .Csirs_.Nzp import Nzp
			self._nzp = Nzp(self._core, self._base)
		return self._nzp

	@property
	def zp(self):
		"""zp commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_zp'):
			from .Csirs_.Zp import Zp
			self._zp = Zp(self._core, self._base)
		return self._zp
