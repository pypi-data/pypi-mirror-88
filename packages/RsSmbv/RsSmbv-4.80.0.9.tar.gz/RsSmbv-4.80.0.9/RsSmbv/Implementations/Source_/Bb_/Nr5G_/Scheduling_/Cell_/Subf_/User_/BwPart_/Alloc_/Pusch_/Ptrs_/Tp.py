from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tp:
	"""Tp commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tp", core, parent)

	def clone(self) -> 'Tp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Tp_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def ngrps(self):
		"""ngrps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ngrps'):
			from .Tp_.Ngrps import Ngrps
			self._ngrps = Ngrps(self._core, self._base)
		return self._ngrps

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Tp_.Scid import Scid
			self._scid = Scid(self._core, self._base)
		return self._scid

	@property
	def sppg(self):
		"""sppg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sppg'):
			from .Tp_.Sppg import Sppg
			self._sppg = Sppg(self._core, self._base)
		return self._sppg

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Tp_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tmDensity(self):
		"""tmDensity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmDensity'):
			from .Tp_.TmDensity import TmDensity
			self._tmDensity = TmDensity(self._core, self._base)
		return self._tmDensity
