from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class E5B:
	"""E5B commands group definition. 11 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("e5B", core, parent)

	def clone(self) -> 'E5B':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = E5B(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .E5B_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def pilot(self):
		"""pilot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pilot'):
			from .E5B_.Pilot import Pilot
			self._pilot = Pilot(self._core, self._base)
		return self._pilot

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .E5B_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .E5B_.State import State
			self._state = State(self._core, self._base)
		return self._state
