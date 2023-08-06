from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Capability:
	"""Capability commands group definition. 16 total commands, 16 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("capability", core, parent)

	def clone(self) -> 'Capability':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Capability(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apsd(self):
		"""apsd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apsd'):
			from .Capability_.Apsd import Apsd
			self._apsd = Apsd(self._core, self._base)
		return self._apsd

	@property
	def cagility(self):
		"""cagility commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cagility'):
			from .Capability_.Cagility import Cagility
			self._cagility = Cagility(self._core, self._base)
		return self._cagility

	@property
	def cpollable(self):
		"""cpollable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpollable'):
			from .Capability_.Cpollable import Cpollable
			self._cpollable = Cpollable(self._core, self._base)
		return self._cpollable

	@property
	def cpRequest(self):
		"""cpRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpRequest'):
			from .Capability_.CpRequest import CpRequest
			self._cpRequest = CpRequest(self._core, self._base)
		return self._cpRequest

	@property
	def dback(self):
		"""dback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dback'):
			from .Capability_.Dback import Dback
			self._dback = Dback(self._core, self._base)
		return self._dback

	@property
	def dofdm(self):
		"""dofdm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dofdm'):
			from .Capability_.Dofdm import Dofdm
			self._dofdm = Dofdm(self._core, self._base)
		return self._dofdm

	@property
	def ess(self):
		"""ess commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ess'):
			from .Capability_.Ess import Ess
			self._ess = Ess(self._core, self._base)
		return self._ess

	@property
	def iback(self):
		"""iback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iback'):
			from .Capability_.Iback import Iback
			self._iback = Iback(self._core, self._base)
		return self._iback

	@property
	def ibss(self):
		"""ibss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibss'):
			from .Capability_.Ibss import Ibss
			self._ibss = Ibss(self._core, self._base)
		return self._ibss

	@property
	def pbcc(self):
		"""pbcc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pbcc'):
			from .Capability_.Pbcc import Pbcc
			self._pbcc = Pbcc(self._core, self._base)
		return self._pbcc

	@property
	def privacy(self):
		"""privacy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_privacy'):
			from .Capability_.Privacy import Privacy
			self._privacy = Privacy(self._core, self._base)
		return self._privacy

	@property
	def qos(self):
		"""qos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qos'):
			from .Capability_.Qos import Qos
			self._qos = Qos(self._core, self._base)
		return self._qos

	@property
	def rmeasurement(self):
		"""rmeasurement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmeasurement'):
			from .Capability_.Rmeasurement import Rmeasurement
			self._rmeasurement = Rmeasurement(self._core, self._base)
		return self._rmeasurement

	@property
	def smgmt(self):
		"""smgmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smgmt'):
			from .Capability_.Smgmt import Smgmt
			self._smgmt = Smgmt(self._core, self._base)
		return self._smgmt

	@property
	def spreamble(self):
		"""spreamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spreamble'):
			from .Capability_.Spreamble import Spreamble
			self._spreamble = Spreamble(self._core, self._base)
		return self._spreamble

	@property
	def sstime(self):
		"""sstime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sstime'):
			from .Capability_.Sstime import Sstime
			self._sstime = Sstime(self._core, self._base)
		return self._sstime
