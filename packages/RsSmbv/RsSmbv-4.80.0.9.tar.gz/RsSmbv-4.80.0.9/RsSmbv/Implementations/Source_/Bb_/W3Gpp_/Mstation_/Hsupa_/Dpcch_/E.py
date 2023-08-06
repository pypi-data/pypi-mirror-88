from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class E:
	"""E commands group definition. 41 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("e", core, parent)

	def clone(self) -> 'E':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = E(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .E_.Ccode import Ccode
			self._ccode = Ccode(self._core, self._base)
		return self._ccode

	@property
	def dtx(self):
		"""dtx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtx'):
			from .E_.Dtx import Dtx
			self._dtx = Dtx(self._core, self._base)
		return self._dtx

	@property
	def frc(self):
		"""frc commands group. 17 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .E_.Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def hbit(self):
		"""hbit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hbit'):
			from .E_.Hbit import Hbit
			self._hbit = Hbit(self._core, self._base)
		return self._hbit

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .E_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def rsNumber(self):
		"""rsNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsNumber'):
			from .E_.RsNumber import RsNumber
			self._rsNumber = RsNumber(self._core, self._base)
		return self._rsNumber

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .E_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tfci(self):
		"""tfci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .E_.Tfci import Tfci
			self._tfci = Tfci(self._core, self._base)
		return self._tfci
