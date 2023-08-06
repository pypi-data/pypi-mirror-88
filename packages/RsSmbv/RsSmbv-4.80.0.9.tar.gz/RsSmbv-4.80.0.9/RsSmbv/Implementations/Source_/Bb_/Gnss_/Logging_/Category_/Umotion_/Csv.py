from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csv:
	"""Csv commands group definition. 21 total commands, 14 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csv", core, parent)

	def clone(self) -> 'Csv':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Csv(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def acceleration(self):
		"""acceleration commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_acceleration'):
			from .Csv_.Acceleration import Acceleration
			self._acceleration = Acceleration(self._core, self._base)
		return self._acceleration

	@property
	def aoffset(self):
		"""aoffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aoffset'):
			from .Csv_.Aoffset import Aoffset
			self._aoffset = Aoffset(self._core, self._base)
		return self._aoffset

	@property
	def attitude(self):
		"""attitude commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_attitude'):
			from .Csv_.Attitude import Attitude
			self._attitude = Attitude(self._core, self._base)
		return self._attitude

	@property
	def gdop(self):
		"""gdop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gdop'):
			from .Csv_.Gdop import Gdop
			self._gdop = Gdop(self._core, self._base)
		return self._gdop

	@property
	def gspeed(self):
		"""gspeed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gspeed'):
			from .Csv_.Gspeed import Gspeed
			self._gspeed = Gspeed(self._core, self._base)
		return self._gspeed

	@property
	def hdop(self):
		"""hdop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hdop'):
			from .Csv_.Hdop import Hdop
			self._hdop = Hdop(self._core, self._base)
		return self._hdop

	@property
	def jerk(self):
		"""jerk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_jerk'):
			from .Csv_.Jerk import Jerk
			self._jerk = Jerk(self._core, self._base)
		return self._jerk

	@property
	def pdop(self):
		"""pdop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdop'):
			from .Csv_.Pdop import Pdop
			self._pdop = Pdop(self._core, self._base)
		return self._pdop

	@property
	def position(self):
		"""position commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_position'):
			from .Csv_.Position import Position
			self._position = Position(self._core, self._base)
		return self._position

	@property
	def select(self):
		"""select commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_select'):
			from .Csv_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	@property
	def svs(self):
		"""svs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svs'):
			from .Csv_.Svs import Svs
			self._svs = Svs(self._core, self._base)
		return self._svs

	@property
	def tdop(self):
		"""tdop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdop'):
			from .Csv_.Tdop import Tdop
			self._tdop = Tdop(self._core, self._base)
		return self._tdop

	@property
	def vdop(self):
		"""vdop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vdop'):
			from .Csv_.Vdop import Vdop
			self._vdop = Vdop(self._core, self._base)
		return self._vdop

	@property
	def velocity(self):
		"""velocity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_velocity'):
			from .Csv_.Velocity import Velocity
			self._velocity = Velocity(self._core, self._base)
		return self._velocity
