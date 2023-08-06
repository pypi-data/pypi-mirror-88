from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psweep:
	"""Psweep commands group definition. 3 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psweep", core, parent)

	def clone(self) -> 'Psweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Psweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_source'):
			from .Psweep_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .Psweep_.Immediate import Immediate
			self._immediate = Immediate(self._core, self._base)
		return self._immediate
