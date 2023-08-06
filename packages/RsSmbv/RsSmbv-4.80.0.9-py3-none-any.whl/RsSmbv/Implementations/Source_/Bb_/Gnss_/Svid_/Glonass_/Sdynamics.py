from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sdynamics:
	"""Sdynamics commands group definition. 12 total commands, 12 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sdynamics", core, parent)

	def clone(self) -> 'Sdynamics':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sdynamics(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def accel(self):
		"""accel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_accel'):
			from .Sdynamics_.Accel import Accel
			self._accel = Accel(self._core, self._base)
		return self._accel

	@property
	def caPeriod(self):
		"""caPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caPeriod'):
			from .Sdynamics_.CaPeriod import CaPeriod
			self._caPeriod = CaPeriod(self._core, self._base)
		return self._caPeriod

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Sdynamics_.Config import Config
			self._config = Config(self._core, self._base)
		return self._config

	@property
	def cphase(self):
		"""cphase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cphase'):
			from .Sdynamics_.Cphase import Cphase
			self._cphase = Cphase(self._core, self._base)
		return self._cphase

	@property
	def cvPeriod(self):
		"""cvPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvPeriod'):
			from .Sdynamics_.CvPeriod import CvPeriod
			self._cvPeriod = CvPeriod(self._core, self._base)
		return self._cvPeriod

	@property
	def ivelocity(self):
		"""ivelocity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ivelocity'):
			from .Sdynamics_.Ivelocity import Ivelocity
			self._ivelocity = Ivelocity(self._core, self._base)
		return self._ivelocity

	@property
	def jerk(self):
		"""jerk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_jerk'):
			from .Sdynamics_.Jerk import Jerk
			self._jerk = Jerk(self._core, self._base)
		return self._jerk

	@property
	def prange(self):
		"""prange commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prange'):
			from .Sdynamics_.Prange import Prange
			self._prange = Prange(self._core, self._base)
		return self._prange

	@property
	def profile(self):
		"""profile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_profile'):
			from .Sdynamics_.Profile import Profile
			self._profile = Profile(self._core, self._base)
		return self._profile

	@property
	def rperiod(self):
		"""rperiod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rperiod'):
			from .Sdynamics_.Rperiod import Rperiod
			self._rperiod = Rperiod(self._core, self._base)
		return self._rperiod

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Sdynamics_.Toffset import Toffset
			self._toffset = Toffset(self._core, self._base)
		return self._toffset

	@property
	def velocity(self):
		"""velocity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_velocity'):
			from .Sdynamics_.Velocity import Velocity
			self._velocity = Velocity(self._core, self._base)
		return self._velocity
