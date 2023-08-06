from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mib:
	"""Mib commands group definition. 10 total commands, 10 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mib", core, parent)

	def clone(self) -> 'Mib':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mib(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def asof(self):
		"""asof commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_asof'):
			from .Mib_.Asof import Asof
			self._asof = Asof(self._core, self._base)
		return self._asof

	@property
	def cbarred(self):
		"""cbarred commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbarred'):
			from .Mib_.Cbarred import Cbarred
			self._cbarred = Cbarred(self._core, self._base)
		return self._cbarred

	@property
	def csZero(self):
		"""csZero commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csZero'):
			from .Mib_.CsZero import CsZero
			self._csZero = CsZero(self._core, self._base)
		return self._csZero

	@property
	def ifrResel(self):
		"""ifrResel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifrResel'):
			from .Mib_.IfrResel import IfrResel
			self._ifrResel = IfrResel(self._core, self._base)
		return self._ifrResel

	@property
	def scOffset(self):
		"""scOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scOffset'):
			from .Mib_.ScOffset import ScOffset
			self._scOffset = ScOffset(self._core, self._base)
		return self._scOffset

	@property
	def scsc(self):
		"""scsc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scsc'):
			from .Mib_.Scsc import Scsc
			self._scsc = Scsc(self._core, self._base)
		return self._scsc

	@property
	def sfOffset(self):
		"""sfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfOffset'):
			from .Mib_.SfOffset import SfOffset
			self._sfOffset = SfOffset(self._core, self._base)
		return self._sfOffset

	@property
	def spare(self):
		"""spare commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spare'):
			from .Mib_.Spare import Spare
			self._spare = Spare(self._core, self._base)
		return self._spare

	@property
	def ssZero(self):
		"""ssZero commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssZero'):
			from .Mib_.SsZero import SsZero
			self._ssZero = SsZero(self._core, self._base)
		return self._ssZero

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Mib_.State import State
			self._state = State(self._core, self._base)
		return self._state
