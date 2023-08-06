from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Simulation:
	"""Simulation commands group definition. 9 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("simulation", core, parent)

	def clone(self) -> 'Simulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Simulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adefinition(self):
		"""adefinition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adefinition'):
			from .Simulation_.Adefinition import Adefinition
			self._adefinition = Adefinition(self._core, self._base)
		return self._adefinition

	@property
	def connector(self):
		"""connector commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connector'):
			from .Simulation_.Connector import Connector
			self._connector = Connector(self._core, self._base)
		return self._connector

	@property
	def delay(self):
		"""delay commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_delay'):
			from .Simulation_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Simulation_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def mretransmissions(self):
		"""mretransmissions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mretransmissions'):
			from .Simulation_.Mretransmissions import Mretransmissions
			self._mretransmissions = Mretransmissions(self._core, self._base)
		return self._mretransmissions

	@property
	def rvZero(self):
		"""rvZero commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvZero'):
			from .Simulation_.RvZero import RvZero
			self._rvZero = RvZero(self._core, self._base)
		return self._rvZero

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Simulation_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Simulation_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern
