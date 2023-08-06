from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToaData:
	"""ToaData commands group definition. 7 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("toaData", core, parent)

	def clone(self) -> 'ToaData':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ToaData(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .ToaData_.Date import Date
			self._date = Date(self._core, self._base)
		return self._date

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .ToaData_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def resolution(self):
		"""resolution commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resolution'):
			from .ToaData_.Resolution import Resolution
			self._resolution = Resolution(self._core, self._base)
		return self._resolution

	@property
	def tbasis(self):
		"""tbasis commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbasis'):
			from .ToaData_.Tbasis import Tbasis
			self._tbasis = Tbasis(self._core, self._base)
		return self._tbasis

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .ToaData_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	@property
	def toWeek(self):
		"""toWeek commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toWeek'):
			from .ToaData_.ToWeek import ToWeek
			self._toWeek = ToWeek(self._core, self._base)
		return self._toWeek

	@property
	def wnumber(self):
		"""wnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wnumber'):
			from .ToaData_.Wnumber import Wnumber
			self._wnumber = Wnumber(self._core, self._base)
		return self._wnumber
