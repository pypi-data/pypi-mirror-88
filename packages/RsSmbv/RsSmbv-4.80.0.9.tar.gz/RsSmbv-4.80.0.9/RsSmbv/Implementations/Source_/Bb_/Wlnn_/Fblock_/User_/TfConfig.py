from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TfConfig:
	"""TfConfig commands group definition. 26 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tfConfig", core, parent)

	def clone(self) -> 'TfConfig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TfConfig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cinfo(self):
		"""cinfo commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_cinfo'):
			from .TfConfig_.Cinfo import Cinfo
			self._cinfo = Cinfo(self._core, self._base)
		return self._cinfo

	@property
	def nuInfo(self):
		"""nuInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nuInfo'):
			from .TfConfig_.NuInfo import NuInfo
			self._nuInfo = NuInfo(self._core, self._base)
		return self._nuInfo

	@property
	def uinfo(self):
		"""uinfo commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_uinfo'):
			from .TfConfig_.Uinfo import Uinfo
			self._uinfo = Uinfo(self._core, self._base)
		return self._uinfo
