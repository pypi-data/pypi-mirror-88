from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 6 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cfactor(self):
		"""cfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfactor'):
			from .Output_.Cfactor import Cfactor
			self._cfactor = Cfactor(self._core, self._base)
		return self._cfactor

	@property
	def error(self):
		"""error commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_error'):
			from .Output_.Error import Error
			self._error = Error(self._core, self._base)
		return self._error

	@property
	def iterations(self):
		"""iterations commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iterations'):
			from .Output_.Iterations import Iterations
			self._iterations = Iterations(self._core, self._base)
		return self._iterations

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Output_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def pep(self):
		"""pep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pep'):
			from .Output_.Pep import Pep
			self._pep = Pep(self._core, self._base)
		return self._pep
