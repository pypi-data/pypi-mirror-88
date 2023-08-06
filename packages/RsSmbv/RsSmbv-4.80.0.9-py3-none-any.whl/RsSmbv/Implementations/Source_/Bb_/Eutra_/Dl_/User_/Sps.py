from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sps:
	"""Sps commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sps", core, parent)

	def clone(self) -> 'Sps':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sps(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def crnti(self):
		"""crnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crnti'):
			from .Sps_.Crnti import Crnti
			self._crnti = Crnti(self._core, self._base)
		return self._crnti

	@property
	def sactivation(self):
		"""sactivation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sactivation'):
			from .Sps_.Sactivation import Sactivation
			self._sactivation = Sactivation(self._core, self._base)
		return self._sactivation

	@property
	def sinterval(self):
		"""sinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinterval'):
			from .Sps_.Sinterval import Sinterval
			self._sinterval = Sinterval(self._core, self._base)
		return self._sinterval

	@property
	def srelease(self):
		"""srelease commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srelease'):
			from .Sps_.Srelease import Srelease
			self._srelease = Srelease(self._core, self._base)
		return self._srelease

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sps_.State import State
			self._state = State(self._core, self._base)
		return self._state
