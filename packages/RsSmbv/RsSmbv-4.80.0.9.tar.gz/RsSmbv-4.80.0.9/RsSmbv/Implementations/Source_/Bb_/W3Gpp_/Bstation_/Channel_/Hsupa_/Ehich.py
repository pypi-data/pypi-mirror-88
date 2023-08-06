from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ehich:
	"""Ehich commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ehich", core, parent)

	def clone(self) -> 'Ehich':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ehich(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Ehich_.Ctype import Ctype
			self._ctype = Ctype(self._core, self._base)
		return self._ctype

	@property
	def dtau(self):
		"""dtau commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dtau'):
			from .Ehich_.Dtau import Dtau
			self._dtau = Dtau(self._core, self._base)
		return self._dtau

	@property
	def etau(self):
		"""etau commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_etau'):
			from .Ehich_.Etau import Etau
			self._etau = Etau(self._core, self._base)
		return self._etau

	@property
	def rgPattern(self):
		"""rgPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rgPattern'):
			from .Ehich_.RgPattern import RgPattern
			self._rgPattern = RgPattern(self._core, self._base)
		return self._rgPattern

	@property
	def ssIndex(self):
		"""ssIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssIndex'):
			from .Ehich_.SsIndex import SsIndex
			self._ssIndex = SsIndex(self._core, self._base)
		return self._ssIndex

	@property
	def ttiedch(self):
		"""ttiedch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiedch'):
			from .Ehich_.Ttiedch import Ttiedch
			self._ttiedch = Ttiedch(self._core, self._base)
		return self._ttiedch
