from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inav:
	"""Inav commands group definition. 49 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inav", core, parent)

	def clone(self) -> 'Inav':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Inav(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccorrection(self):
		"""ccorrection commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccorrection'):
			from .Inav_.Ccorrection import Ccorrection
			self._ccorrection = Ccorrection(self._core, self._base)
		return self._ccorrection

	@property
	def e1Bdvs(self):
		"""e1Bdvs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Bdvs'):
			from .Inav_.E1Bdvs import E1Bdvs
			self._e1Bdvs = E1Bdvs(self._core, self._base)
		return self._e1Bdvs

	@property
	def e1Bhs(self):
		"""e1Bhs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Bhs'):
			from .Inav_.E1Bhs import E1Bhs
			self._e1Bhs = E1Bhs(self._core, self._base)
		return self._e1Bhs

	@property
	def e5Bdvs(self):
		"""e5Bdvs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Bdvs'):
			from .Inav_.E5Bdvs import E5Bdvs
			self._e5Bdvs = E5Bdvs(self._core, self._base)
		return self._e5Bdvs

	@property
	def e5Bhs(self):
		"""e5Bhs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Bhs'):
			from .Inav_.E5Bhs import E5Bhs
			self._e5Bhs = E5Bhs(self._core, self._base)
		return self._e5Bhs

	@property
	def ephemeris(self):
		"""ephemeris commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Inav_.Ephemeris import Ephemeris
			self._ephemeris = Ephemeris(self._core, self._base)
		return self._ephemeris
