from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptrs:
	"""Ptrs commands group definition. 17 total commands, 10 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptrs", core, parent)

	def clone(self) -> 'Ptrs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ptrs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mcs1(self):
		"""mcs1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs1'):
			from .Ptrs_.Mcs1 import Mcs1
			self._mcs1 = Mcs1(self._core, self._base)
		return self._mcs1

	@property
	def mcs2(self):
		"""mcs2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs2'):
			from .Ptrs_.Mcs2 import Mcs2
			self._mcs2 = Mcs2(self._core, self._base)
		return self._mcs2

	@property
	def mcs3(self):
		"""mcs3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs3'):
			from .Ptrs_.Mcs3 import Mcs3
			self._mcs3 = Mcs3(self._core, self._base)
		return self._mcs3

	@property
	def port(self):
		"""port commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_port'):
			from .Ptrs_.Port import Port
			self._port = Port(self._core, self._base)
		return self._port

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Ptrs_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def rb0(self):
		"""rb0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rb0'):
			from .Ptrs_.Rb0 import Rb0
			self._rb0 = Rb0(self._core, self._base)
		return self._rb0

	@property
	def rb1(self):
		"""rb1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rb1'):
			from .Ptrs_.Rb1 import Rb1
			self._rb1 = Rb1(self._core, self._base)
		return self._rb1

	@property
	def reof(self):
		"""reof commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reof'):
			from .Ptrs_.Reof import Reof
			self._reof = Reof(self._core, self._base)
		return self._reof

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Ptrs_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tp(self):
		"""tp commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_tp'):
			from .Ptrs_.Tp import Tp
			self._tp = Tp(self._core, self._base)
		return self._tp
