from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hs:
	"""Hs commands group definition. 45 total commands, 20 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hs", core, parent)

	def clone(self) -> 'Hs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Hs_.Ccode import Ccode
			self._ccode = Ccode(self._core, self._base)
		return self._ccode

	@property
	def compatibility(self):
		"""compatibility commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_compatibility'):
			from .Hs_.Compatibility import Compatibility
			self._compatibility = Compatibility(self._core, self._base)
		return self._compatibility

	@property
	def cqi(self):
		"""cqi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Hs_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def hack(self):
		"""hack commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hack'):
			from .Hs_.Hack import Hack
			self._hack = Hack(self._core, self._base)
		return self._hack

	@property
	def haPattern(self):
		"""haPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_haPattern'):
			from .Hs_.HaPattern import HaPattern
			self._haPattern = HaPattern(self._core, self._base)
		return self._haPattern

	@property
	def mimo(self):
		"""mimo commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .Hs_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def mmode(self):
		"""mmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmode'):
			from .Hs_.Mmode import Mmode
			self._mmode = Mmode(self._core, self._base)
		return self._mmode

	@property
	def pcqi(self):
		"""pcqi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcqi'):
			from .Hs_.Pcqi import Pcqi
			self._pcqi = Pcqi(self._core, self._base)
		return self._pcqi

	@property
	def poAck(self):
		"""poAck commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poAck'):
			from .Hs_.PoAck import PoAck
			self._poAck = PoAck(self._core, self._base)
		return self._poAck

	@property
	def poNack(self):
		"""poNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poNack'):
			from .Hs_.PoNack import PoNack
			self._poNack = PoNack(self._core, self._base)
		return self._poNack

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Hs_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def row(self):
		"""row commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Hs_.Row import Row
			self._row = Row(self._core, self._base)
		return self._row

	@property
	def rowcount(self):
		"""rowcount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rowcount'):
			from .Hs_.Rowcount import Rowcount
			self._rowcount = Rowcount(self._core, self._base)
		return self._rowcount

	@property
	def sc(self):
		"""sc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sc'):
			from .Hs_.Sc import Sc
			self._sc = Sc(self._core, self._base)
		return self._sc

	@property
	def scActive(self):
		"""scActive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scActive'):
			from .Hs_.ScActive import ScActive
			self._scActive = ScActive(self._core, self._base)
		return self._scActive

	@property
	def sdelay(self):
		"""sdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdelay'):
			from .Hs_.Sdelay import Sdelay
			self._sdelay = Sdelay(self._core, self._base)
		return self._sdelay

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Hs_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def slength(self):
		"""slength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Hs_.Slength import Slength
			self._slength = Slength(self._core, self._base)
		return self._slength

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Hs_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def ttiDistance(self):
		"""ttiDistance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiDistance'):
			from .Hs_.TtiDistance import TtiDistance
			self._ttiDistance = TtiDistance(self._core, self._base)
		return self._ttiDistance
