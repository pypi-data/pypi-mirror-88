from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsch:
	"""Hsch commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsch", core, parent)

	def clone(self) -> 'Hsch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cvpb(self):
		"""cvpb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvpb'):
			from .Hsch_.Cvpb import Cvpb
			self._cvpb = Cvpb(self._core, self._base)
		return self._cvpb

	@property
	def prsr(self):
		"""prsr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prsr'):
			from .Hsch_.Prsr import Prsr
			self._prsr = Prsr(self._core, self._base)
		return self._prsr

	@property
	def psbs(self):
		"""psbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psbs'):
			from .Hsch_.Psbs import Psbs
			self._psbs = Psbs(self._core, self._base)
		return self._psbs

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .Hsch_.RvParameter import RvParameter
			self._rvParameter = RvParameter(self._core, self._base)
		return self._rvParameter
