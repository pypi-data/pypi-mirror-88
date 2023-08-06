from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpControl:
	"""DpControl commands group definition. 8 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpControl", core, parent)

	def clone(self) -> 'DpControl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpControl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .DpControl_.Direction import Direction
			self._direction = Direction(self._core, self._base)
		return self._direction

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .DpControl_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def range(self):
		"""range commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_range'):
			from .DpControl_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .DpControl_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def step(self):
		"""step commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_step'):
			from .DpControl_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .DpControl_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power
