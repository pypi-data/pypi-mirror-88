from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpch:
	"""Dpch commands group definition. 36 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpch", core, parent)

	def clone(self) -> 'Dpch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccoding(self):
		"""ccoding commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Dpch_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def derror(self):
		"""derror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_derror'):
			from .Dpch_.Derror import Derror
			self._derror = Derror(self._core, self._base)
		return self._derror

	@property
	def dpControl(self):
		"""dpControl commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpControl'):
			from .Dpch_.DpControl import DpControl
			self._dpControl = DpControl(self._core, self._base)
		return self._dpControl

	@property
	def interleaver2(self):
		"""interleaver2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interleaver2'):
			from .Dpch_.Interleaver2 import Interleaver2
			self._interleaver2 = Interleaver2(self._core, self._base)
		return self._interleaver2

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dpch_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tchannel(self):
		"""tchannel commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_tchannel'):
			from .Dpch_.Tchannel import Tchannel
			self._tchannel = Tchannel(self._core, self._base)
		return self._tchannel
