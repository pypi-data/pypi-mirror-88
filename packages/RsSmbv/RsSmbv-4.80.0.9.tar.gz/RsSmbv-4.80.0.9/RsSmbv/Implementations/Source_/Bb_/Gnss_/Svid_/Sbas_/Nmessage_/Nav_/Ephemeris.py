from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ephemeris:
	"""Ephemeris commands group definition. 21 total commands, 11 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ephemeris", core, parent)

	def clone(self) -> 'Ephemeris':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ephemeris(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def toe(self):
		"""toe commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_toe'):
			from .Ephemeris_.Toe import Toe
			self._toe = Toe(self._core, self._base)
		return self._toe

	@property
	def ura(self):
		"""ura commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ura'):
			from .Ephemeris_.Ura import Ura
			self._ura = Ura(self._core, self._base)
		return self._ura

	@property
	def xddn(self):
		"""xddn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xddn'):
			from .Ephemeris_.Xddn import Xddn
			self._xddn = Xddn(self._core, self._base)
		return self._xddn

	@property
	def xdn(self):
		"""xdn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xdn'):
			from .Ephemeris_.Xdn import Xdn
			self._xdn = Xdn(self._core, self._base)
		return self._xdn

	@property
	def xn(self):
		"""xn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xn'):
			from .Ephemeris_.Xn import Xn
			self._xn = Xn(self._core, self._base)
		return self._xn

	@property
	def yddn(self):
		"""yddn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_yddn'):
			from .Ephemeris_.Yddn import Yddn
			self._yddn = Yddn(self._core, self._base)
		return self._yddn

	@property
	def ydn(self):
		"""ydn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ydn'):
			from .Ephemeris_.Ydn import Ydn
			self._ydn = Ydn(self._core, self._base)
		return self._ydn

	@property
	def yn(self):
		"""yn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_yn'):
			from .Ephemeris_.Yn import Yn
			self._yn = Yn(self._core, self._base)
		return self._yn

	@property
	def zddn(self):
		"""zddn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_zddn'):
			from .Ephemeris_.Zddn import Zddn
			self._zddn = Zddn(self._core, self._base)
		return self._zddn

	@property
	def zdn(self):
		"""zdn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_zdn'):
			from .Ephemeris_.Zdn import Zdn
			self._zdn = Zdn(self._core, self._base)
		return self._zdn

	@property
	def zn(self):
		"""zn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_zn'):
			from .Ephemeris_.Zn import Zn
			self._zn = Zn(self._core, self._base)
		return self._zn
