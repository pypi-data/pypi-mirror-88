from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sl:
	"""Sl commands group definition. 89 total commands, 16 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sl", core, parent)

	def clone(self) -> 'Sl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alloc(self):
		"""alloc commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Sl_.Alloc import Alloc
			self._alloc = Alloc(self._core, self._base)
		return self._alloc

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Sl_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Sl_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Sl_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def nalloc(self):
		"""nalloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nalloc'):
			from .Sl_.Nalloc import Nalloc
			self._nalloc = Nalloc(self._core, self._base)
		return self._nalloc

	@property
	def nsci(self):
		"""nsci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsci'):
			from .Sl_.Nsci import Nsci
			self._nsci = Nsci(self._core, self._base)
		return self._nsci

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Sl_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def rctrl(self):
		"""rctrl commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rctrl'):
			from .Sl_.Rctrl import Rctrl
			self._rctrl = Rctrl(self._core, self._base)
		return self._rctrl

	@property
	def rdata(self):
		"""rdata commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_rdata'):
			from .Sl_.Rdata import Rdata
			self._rdata = Rdata(self._core, self._base)
		return self._rdata

	@property
	def rdisc(self):
		"""rdisc commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_rdisc'):
			from .Sl_.Rdisc import Rdisc
			self._rdisc = Rdisc(self._core, self._base)
		return self._rdisc

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .Sl_.Restart import Restart
			self._restart = Restart(self._core, self._base)
		return self._restart

	@property
	def rmc(self):
		"""rmc commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rmc'):
			from .Sl_.Rmc import Rmc
			self._rmc = Rmc(self._core, self._base)
		return self._rmc

	@property
	def sci(self):
		"""sci commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_sci'):
			from .Sl_.Sci import Sci
			self._sci = Sci(self._core, self._base)
		return self._sci

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sl_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def sync(self):
		"""sync commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Sl_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	@property
	def v2X(self):
		"""v2X commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_v2X'):
			from .Sl_.V2X import V2X
			self._v2X = V2X(self._core, self._base)
		return self._v2X
