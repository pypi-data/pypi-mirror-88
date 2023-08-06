from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nav:
	"""Nav commands group definition. 23 total commands, 12 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nav", core, parent)

	def clone(self) -> 'Nav':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nav(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def almanac(self):
		"""almanac commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_almanac'):
			from .Nav_.Almanac import Almanac
			self._almanac = Almanac(self._core, self._base)
		return self._almanac

	@property
	def ceCovariance(self):
		"""ceCovariance commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ceCovariance'):
			from .Nav_.CeCovariance import CeCovariance
			self._ceCovariance = CeCovariance(self._core, self._base)
		return self._ceCovariance

	@property
	def dfactor(self):
		"""dfactor commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dfactor'):
			from .Nav_.Dfactor import Dfactor
			self._dfactor = Dfactor(self._core, self._base)
		return self._dfactor

	@property
	def fcDegradation(self):
		"""fcDegradation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcDegradation'):
			from .Nav_.FcDegradation import FcDegradation
			self._fcDegradation = FcDegradation(self._core, self._base)
		return self._fcDegradation

	@property
	def fcorrection(self):
		"""fcorrection commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcorrection'):
			from .Nav_.Fcorrection import Fcorrection
			self._fcorrection = Fcorrection(self._core, self._base)
		return self._fcorrection

	@property
	def igrid(self):
		"""igrid commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_igrid'):
			from .Nav_.Igrid import Igrid
			self._igrid = Igrid(self._core, self._base)
		return self._igrid

	@property
	def ltCorrection(self):
		"""ltCorrection commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ltCorrection'):
			from .Nav_.LtCorrection import LtCorrection
			self._ltCorrection = LtCorrection(self._core, self._base)
		return self._ltCorrection

	@property
	def prNoise(self):
		"""prNoise commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_prNoise'):
			from .Nav_.PrNoise import PrNoise
			self._prNoise = PrNoise(self._core, self._base)
		return self._prNoise

	@property
	def prnMask(self):
		"""prnMask commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_prnMask'):
			from .Nav_.PrnMask import PrnMask
			self._prnMask = PrnMask(self._core, self._base)
		return self._prnMask

	@property
	def rinex(self):
		"""rinex commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rinex'):
			from .Nav_.Rinex import Rinex
			self._rinex = Rinex(self._core, self._base)
		return self._rinex

	@property
	def service(self):
		"""service commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_service'):
			from .Nav_.Service import Service
			self._service = Service(self._core, self._base)
		return self._service

	@property
	def utcOffset(self):
		"""utcOffset commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_utcOffset'):
			from .Nav_.UtcOffset import UtcOffset
			self._utcOffset = UtcOffset(self._core, self._base)
		return self._utcOffset
