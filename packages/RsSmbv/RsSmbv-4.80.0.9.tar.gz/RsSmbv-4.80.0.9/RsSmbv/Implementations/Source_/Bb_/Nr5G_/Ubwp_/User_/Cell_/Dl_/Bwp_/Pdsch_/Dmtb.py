from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmtb:
	"""Dmtb commands group definition. 13 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmtb", core, parent)

	def clone(self) -> 'Dmtb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dmtb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apIndex(self):
		"""apIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apIndex'):
			from .Dmtb_.ApIndex import ApIndex
			self._apIndex = ApIndex(self._core, self._base)
		return self._apIndex

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Dmtb_.Ctype import Ctype
			self._ctype = Ctype(self._core, self._base)
		return self._ctype

	@property
	def mlength(self):
		"""mlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlength'):
			from .Dmtb_.Mlength import Mlength
			self._mlength = Mlength(self._core, self._base)
		return self._mlength

	@property
	def ptrs(self):
		"""ptrs commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptrs'):
			from .Dmtb_.Ptrs import Ptrs
			self._ptrs = Ptrs(self._core, self._base)
		return self._ptrs

	@property
	def sid0(self):
		"""sid0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sid0'):
			from .Dmtb_.Sid0 import Sid0
			self._sid0 = Sid0(self._core, self._base)
		return self._sid0

	@property
	def sid1(self):
		"""sid1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sid1'):
			from .Dmtb_.Sid1 import Sid1
			self._sid1 = Sid1(self._core, self._base)
		return self._sid1
