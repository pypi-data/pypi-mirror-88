from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Smapping:
	"""Smapping commands group definition. 6 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("smapping", core, parent)

	def clone(self) -> 'Smapping':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Smapping(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bselection(self):
		"""bselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bselection'):
			from .Smapping_.Bselection import Bselection
			self._bselection = Bselection(self._core, self._base)
		return self._bselection

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Smapping_.Index import Index
			self._index = Index(self._core, self._base)
		return self._index

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Smapping_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def row(self):
		"""row commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Smapping_.Row import Row
			self._row = Row(self._core, self._base)
		return self._row

	@property
	def tshift(self):
		"""tshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tshift'):
			from .Smapping_.Tshift import Tshift
			self._tshift = Tshift(self._core, self._base)
		return self._tshift
