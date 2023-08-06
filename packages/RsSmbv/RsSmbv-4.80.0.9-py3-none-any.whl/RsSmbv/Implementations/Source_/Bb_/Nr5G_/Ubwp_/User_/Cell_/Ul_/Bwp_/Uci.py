from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uci:
	"""Uci commands group definition. 10 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uci", core, parent)

	def clone(self) -> 'Uci':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Uci(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alpha(self):
		"""alpha commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alpha'):
			from .Uci_.Alpha import Alpha
			self._alpha = Alpha(self._core, self._base)
		return self._alpha

	@property
	def csi(self):
		"""csi commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_csi'):
			from .Uci_.Csi import Csi
			self._csi = Csi(self._core, self._base)
		return self._csi

	@property
	def harq(self):
		"""harq commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Uci_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Uci_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Uci_.State import State
			self._state = State(self._core, self._base)
		return self._state
