from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rmc:
	"""Rmc commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmc", core, parent)

	def clone(self) -> 'Rmc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rmc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def arblocks(self):
		"""arblocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_arblocks'):
			from .Rmc_.Arblocks import Arblocks
			self._arblocks = Arblocks(self._core, self._base)
		return self._arblocks

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Rmc_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def paySize(self):
		"""paySize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paySize'):
			from .Rmc_.PaySize import PaySize
			self._paySize = PaySize(self._core, self._base)
		return self._paySize

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Rmc_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def rmc(self):
		"""rmc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmc'):
			from .Rmc_.Rmc import Rmc
			self._rmc = Rmc(self._core, self._base)
		return self._rmc

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Rmc_.State import State
			self._state = State(self._core, self._base)
		return self._state
