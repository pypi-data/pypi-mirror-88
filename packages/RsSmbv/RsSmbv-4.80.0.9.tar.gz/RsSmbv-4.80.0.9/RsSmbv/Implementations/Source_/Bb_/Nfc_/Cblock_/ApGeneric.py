from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApGeneric:
	"""ApGeneric commands group definition. 9 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apGeneric", core, parent)

	def clone(self) -> 'ApGeneric':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApGeneric(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bodata(self):
		"""bodata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bodata'):
			from .ApGeneric_.Bodata import Bodata
			self._bodata = Bodata(self._core, self._base)
		return self._bodata

	@property
	def boLength(self):
		"""boLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boLength'):
			from .ApGeneric_.BoLength import BoLength
			self._boLength = BoLength(self._core, self._base)
		return self._boLength

	@property
	def ftype(self):
		"""ftype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ftype'):
			from .ApGeneric_.Ftype import Ftype
			self._ftype = Ftype(self._core, self._base)
		return self._ftype

	@property
	def shdata(self):
		"""shdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shdata'):
			from .ApGeneric_.Shdata import Shdata
			self._shdata = Shdata(self._core, self._base)
		return self._shdata

	@property
	def shLength(self):
		"""shLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shLength'):
			from .ApGeneric_.ShLength import ShLength
			self._shLength = ShLength(self._core, self._base)
		return self._shLength

	@property
	def stdLength(self):
		"""stdLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stdLength'):
			from .ApGeneric_.StdLength import StdLength
			self._stdLength = StdLength(self._core, self._base)
		return self._stdLength

	@property
	def stdata(self):
		"""stdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stdata'):
			from .ApGeneric_.Stdata import Stdata
			self._stdata = Stdata(self._core, self._base)
		return self._stdata

	@property
	def stePresent(self):
		"""stePresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stePresent'):
			from .ApGeneric_.StePresent import StePresent
			self._stePresent = StePresent(self._core, self._base)
		return self._stePresent

	@property
	def stpLength(self):
		"""stpLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stpLength'):
			from .ApGeneric_.StpLength import StpLength
			self._stpLength = StpLength(self._core, self._base)
		return self._stpLength
