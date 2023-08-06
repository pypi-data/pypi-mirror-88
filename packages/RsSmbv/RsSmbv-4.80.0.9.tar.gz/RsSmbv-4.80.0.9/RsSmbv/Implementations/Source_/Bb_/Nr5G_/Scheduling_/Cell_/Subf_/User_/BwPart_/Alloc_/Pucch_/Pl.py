from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pl:
	"""Pl commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pl", core, parent)

	def clone(self) -> 'Pl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ack(self):
		"""ack commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ack'):
			from .Pl_.Ack import Ack
			self._ack = Ack(self._core, self._base)
		return self._ack

	@property
	def srCount(self):
		"""srCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srCount'):
			from .Pl_.SrCount import SrCount
			self._srCount = SrCount(self._core, self._base)
		return self._srCount

	@property
	def uci(self):
		"""uci commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_uci'):
			from .Pl_.Uci import Uci
			self._uci = Uci(self._core, self._base)
		return self._uci
