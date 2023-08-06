from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsich:
	"""Hsich commands group definition. 4 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsich", core, parent)

	def clone(self) -> 'Hsich':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsich(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def anPattern(self):
		"""anPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anPattern'):
			from .Hsich_.AnPattern import AnPattern
			self._anPattern = AnPattern(self._core, self._base)
		return self._anPattern

	@property
	def cqi(self):
		"""cqi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Hsich_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .Hsich_.TtInterval import TtInterval
			self._ttInterval = TtInterval(self._core, self._base)
		return self._ttInterval
