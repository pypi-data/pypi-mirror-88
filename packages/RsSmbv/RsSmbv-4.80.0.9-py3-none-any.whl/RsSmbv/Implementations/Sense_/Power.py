from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 24 total commands, 14 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aperture(self):
		"""aperture commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_aperture'):
			from .Power_.Aperture import Aperture
			self._aperture = Aperture(self._core, self._base)
		return self._aperture

	@property
	def correction(self):
		"""correction commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_correction'):
			from .Power_.Correction import Correction
			self._correction = Correction(self._core, self._base)
		return self._correction

	@property
	def direct(self):
		"""direct commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direct'):
			from .Power_.Direct import Direct
			self._direct = Direct(self._core, self._base)
		return self._direct

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Power_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def filterPy(self):
		"""filterPy commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .Power_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Power_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def logging(self):
		"""logging commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_logging'):
			from .Power_.Logging import Logging
			self._logging = Logging(self._core, self._base)
		return self._logging

	@property
	def offset(self):
		"""offset commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Power_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Power_.Snumber import Snumber
			self._snumber = Snumber(self._core, self._base)
		return self._snumber

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Power_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def status(self):
		"""status commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_status'):
			from .Power_.Status import Status
			self._status = Status(self._core, self._base)
		return self._status

	@property
	def sversion(self):
		"""sversion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sversion'):
			from .Power_.Sversion import Sversion
			self._sversion = Sversion(self._core, self._base)
		return self._sversion

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Power_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def zero(self):
		"""zero commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zero'):
			from .Power_.Zero import Zero
			self._zero = Zero(self._core, self._base)
		return self._zero
