from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DumRes:
	"""DumRes commands group definition. 9 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dumRes", core, parent)

	def clone(self) -> 'DumRes':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DumRes(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .DumRes_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .DumRes_.Dlist import Dlist
			self._dlist = Dlist(self._core, self._base)
		return self._dlist

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .DumRes_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .DumRes_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .DumRes_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .DumRes_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def sltFmt(self):
		"""sltFmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sltFmt'):
			from .DumRes_.SltFmt import SltFmt
			self._sltFmt = SltFmt(self._core, self._base)
		return self._sltFmt

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .DumRes_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tpState(self):
		"""tpState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpState'):
			from .DumRes_.TpState import TpState
			self._tpState = TpState(self._core, self._base)
		return self._tpState
