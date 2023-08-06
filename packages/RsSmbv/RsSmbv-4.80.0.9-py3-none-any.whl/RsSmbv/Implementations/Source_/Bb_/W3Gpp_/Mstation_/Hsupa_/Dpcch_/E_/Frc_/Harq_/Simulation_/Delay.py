from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def clone(self) -> 'Delay':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Delay(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def auser(self):
		"""auser commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auser'):
			from .Delay_.Auser import Auser
			self._auser = Auser(self._core, self._base)
		return self._auser

	@property
	def feedback(self):
		"""feedback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_feedback'):
			from .Delay_.Feedback import Feedback
			self._feedback = Feedback(self._core, self._base)
		return self._feedback
