from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phich:
	"""Phich commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phich", core, parent)

	def clone(self) -> 'Phich':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Phich(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Phich_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def ngParameter(self):
		"""ngParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ngParameter'):
			from .Phich_.NgParameter import NgParameter
			self._ngParameter = NgParameter(self._core, self._base)
		return self._ngParameter
