from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fnav:
	"""Fnav commands group definition. 44 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fnav", core, parent)

	def clone(self) -> 'Fnav':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fnav(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccorrection(self):
		"""ccorrection commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccorrection'):
			from .Fnav_.Ccorrection import Ccorrection
			self._ccorrection = Ccorrection(self._core, self._base)
		return self._ccorrection

	@property
	def e5Advs(self):
		"""e5Advs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Advs'):
			from .Fnav_.E5Advs import E5Advs
			self._e5Advs = E5Advs(self._core, self._base)
		return self._e5Advs

	@property
	def e5Ahs(self):
		"""e5Ahs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Ahs'):
			from .Fnav_.E5Ahs import E5Ahs
			self._e5Ahs = E5Ahs(self._core, self._base)
		return self._e5Ahs

	@property
	def ephemeris(self):
		"""ephemeris commands group. 18 Sub-classes, 0 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Fnav_.Ephemeris import Ephemeris
			self._ephemeris = Ephemeris(self._core, self._base)
		return self._ephemeris
