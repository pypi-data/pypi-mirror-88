from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EhFlags:
	"""EhFlags commands group definition. 7 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ehFlags", core, parent)

	def clone(self) -> 'EhFlags':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EhFlags(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aaddress(self):
		"""aaddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aaddress'):
			from .EhFlags_.Aaddress import Aaddress
			self._aaddress = Aaddress(self._core, self._base)
		return self._aaddress

	@property
	def adInfo(self):
		"""adInfo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adInfo'):
			from .EhFlags_.AdInfo import AdInfo
			self._adInfo = AdInfo(self._core, self._base)
		return self._adInfo

	@property
	def aptr(self):
		"""aptr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aptr'):
			from .EhFlags_.Aptr import Aptr
			self._aptr = Aptr(self._core, self._base)
		return self._aptr

	@property
	def cinfo(self):
		"""cinfo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cinfo'):
			from .EhFlags_.Cinfo import Cinfo
			self._cinfo = Cinfo(self._core, self._base)
		return self._cinfo

	@property
	def sinfo(self):
		"""sinfo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sinfo'):
			from .EhFlags_.Sinfo import Sinfo
			self._sinfo = Sinfo(self._core, self._base)
		return self._sinfo

	@property
	def taddress(self):
		"""taddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_taddress'):
			from .EhFlags_.Taddress import Taddress
			self._taddress = Taddress(self._core, self._base)
		return self._taddress

	@property
	def tpower(self):
		"""tpower commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpower'):
			from .EhFlags_.Tpower import Tpower
			self._tpower = Tpower(self._core, self._base)
		return self._tpower
