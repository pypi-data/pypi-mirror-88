from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Orbit:
	"""Orbit commands group definition. 11 total commands, 11 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("orbit", core, parent)

	def clone(self) -> 'Orbit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Orbit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Orbit_.Date import Date
			self._date = Date(self._core, self._base)
		return self._date

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Orbit_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	@property
	def xddn(self):
		"""xddn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xddn'):
			from .Orbit_.Xddn import Xddn
			self._xddn = Xddn(self._core, self._base)
		return self._xddn

	@property
	def xdn(self):
		"""xdn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xdn'):
			from .Orbit_.Xdn import Xdn
			self._xdn = Xdn(self._core, self._base)
		return self._xdn

	@property
	def xn(self):
		"""xn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xn'):
			from .Orbit_.Xn import Xn
			self._xn = Xn(self._core, self._base)
		return self._xn

	@property
	def yddn(self):
		"""yddn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yddn'):
			from .Orbit_.Yddn import Yddn
			self._yddn = Yddn(self._core, self._base)
		return self._yddn

	@property
	def ydn(self):
		"""ydn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ydn'):
			from .Orbit_.Ydn import Ydn
			self._ydn = Ydn(self._core, self._base)
		return self._ydn

	@property
	def yn(self):
		"""yn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yn'):
			from .Orbit_.Yn import Yn
			self._yn = Yn(self._core, self._base)
		return self._yn

	@property
	def zddn(self):
		"""zddn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zddn'):
			from .Orbit_.Zddn import Zddn
			self._zddn = Zddn(self._core, self._base)
		return self._zddn

	@property
	def zdn(self):
		"""zdn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zdn'):
			from .Orbit_.Zdn import Zdn
			self._zdn = Zdn(self._core, self._base)
		return self._zdn

	@property
	def zn(self):
		"""zn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zn'):
			from .Orbit_.Zn import Zn
			self._zn = Zn(self._core, self._base)
		return self._zn
