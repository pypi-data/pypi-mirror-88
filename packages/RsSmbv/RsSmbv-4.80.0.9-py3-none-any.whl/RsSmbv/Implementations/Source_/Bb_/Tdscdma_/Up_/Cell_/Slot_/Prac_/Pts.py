from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pts:
	"""Pts commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pts", core, parent)

	def clone(self) -> 'Pts':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pts(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def distance(self):
		"""distance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_distance'):
			from .Pts_.Distance import Distance
			self._distance = Distance(self._core, self._base)
		return self._distance

	@property
	def pcorrection(self):
		"""pcorrection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcorrection'):
			from .Pts_.Pcorrection import Pcorrection
			self._pcorrection = Pcorrection(self._core, self._base)
		return self._pcorrection

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Pts_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pstep(self):
		"""pstep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pstep'):
			from .Pts_.Pstep import Pstep
			self._pstep = Pstep(self._core, self._base)
		return self._pstep

	@property
	def repetition(self):
		"""repetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetition'):
			from .Pts_.Repetition import Repetition
			self._repetition = Repetition(self._core, self._base)
		return self._repetition

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Pts_.Start import Start
			self._start = Start(self._core, self._base)
		return self._start
