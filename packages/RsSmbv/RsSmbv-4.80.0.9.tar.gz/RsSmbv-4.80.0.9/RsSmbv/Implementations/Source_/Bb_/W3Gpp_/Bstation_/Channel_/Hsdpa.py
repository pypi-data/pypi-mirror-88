from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsdpa:
	"""Hsdpa commands group definition. 48 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsdpa", core, parent)

	def clone(self) -> 'Hsdpa':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsdpa(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bmode(self):
		"""bmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bmode'):
			from .Hsdpa_.Bmode import Bmode
			self._bmode = Bmode(self._core, self._base)
		return self._bmode

	@property
	def cvpb(self):
		"""cvpb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvpb'):
			from .Hsdpa_.Cvpb import Cvpb
			self._cvpb = Cvpb(self._core, self._base)
		return self._cvpb

	@property
	def hset(self):
		"""hset commands group. 29 Sub-classes, 2 commands."""
		if not hasattr(self, '_hset'):
			from .Hsdpa_.Hset import Hset
			self._hset = Hset(self._core, self._base)
		return self._hset

	@property
	def mimo(self):
		"""mimo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .Hsdpa_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Hsdpa_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def prsr(self):
		"""prsr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prsr'):
			from .Hsdpa_.Prsr import Prsr
			self._prsr = Prsr(self._core, self._base)
		return self._prsr

	@property
	def psbs(self):
		"""psbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psbs'):
			from .Hsdpa_.Psbs import Psbs
			self._psbs = Psbs(self._core, self._base)
		return self._psbs

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Hsdpa_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def ttiDistance(self):
		"""ttiDistance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiDistance'):
			from .Hsdpa_.TtiDistance import TtiDistance
			self._ttiDistance = TtiDistance(self._core, self._base)
		return self._ttiDistance
