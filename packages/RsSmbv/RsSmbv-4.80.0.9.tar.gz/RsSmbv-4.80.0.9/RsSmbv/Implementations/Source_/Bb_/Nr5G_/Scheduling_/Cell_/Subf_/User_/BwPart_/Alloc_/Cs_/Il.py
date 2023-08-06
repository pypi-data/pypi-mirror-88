from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Il:
	"""Il commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("il", core, parent)

	def clone(self) -> 'Il':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Il(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bunSize(self):
		"""bunSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bunSize'):
			from .Il_.BunSize import BunSize
			self._bunSize = BunSize(self._core, self._base)
		return self._bunSize

	@property
	def shidx(self):
		"""shidx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shidx'):
			from .Il_.Shidx import Shidx
			self._shidx = Shidx(self._core, self._base)
		return self._shidx

	@property
	def size(self):
		"""size commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_size'):
			from .Il_.Size import Size
			self._size = Size(self._core, self._base)
		return self._size

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Il_.State import State
			self._state = State(self._core, self._base)
		return self._state
