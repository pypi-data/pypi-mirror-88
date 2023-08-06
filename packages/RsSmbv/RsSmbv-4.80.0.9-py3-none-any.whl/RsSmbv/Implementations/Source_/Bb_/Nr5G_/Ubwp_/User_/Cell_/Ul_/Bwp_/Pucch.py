from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 5 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pucch", core, parent)

	def clone(self) -> 'Pucch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pucch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adMrs(self):
		"""adMrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adMrs'):
			from .Pucch_.AdMrs import AdMrs
			self._adMrs = AdMrs(self._core, self._base)
		return self._adMrs

	@property
	def bpsk(self):
		"""bpsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpsk'):
			from .Pucch_.Bpsk import Bpsk
			self._bpsk = Bpsk(self._core, self._base)
		return self._bpsk

	@property
	def hack(self):
		"""hack commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hack'):
			from .Pucch_.Hack import Hack
			self._hack = Hack(self._core, self._base)
		return self._hack

	@property
	def pdsharq(self):
		"""pdsharq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsharq'):
			from .Pucch_.Pdsharq import Pdsharq
			self._pdsharq = Pdsharq(self._core, self._base)
		return self._pdsharq
