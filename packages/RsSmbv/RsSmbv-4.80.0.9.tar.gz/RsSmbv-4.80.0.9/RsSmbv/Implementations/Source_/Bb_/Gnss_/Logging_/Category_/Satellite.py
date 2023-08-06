from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Satellite:
	"""Satellite commands group definition. 22 total commands, 20 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("satellite", core, parent)

	def clone(self) -> 'Satellite':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Satellite(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def acceleration(self):
		"""acceleration commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_acceleration'):
			from .Satellite_.Acceleration import Acceleration
			self._acceleration = Acceleration(self._core, self._base)
		return self._acceleration

	@property
	def azimuth(self):
		"""azimuth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_azimuth'):
			from .Satellite_.Azimuth import Azimuth
			self._azimuth = Azimuth(self._core, self._base)
		return self._azimuth

	@property
	def cbias(self):
		"""cbias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbias'):
			from .Satellite_.Cbias import Cbias
			self._cbias = Cbias(self._core, self._base)
		return self._cbias

	@property
	def cphase(self):
		"""cphase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cphase'):
			from .Satellite_.Cphase import Cphase
			self._cphase = Cphase(self._core, self._base)
		return self._cphase

	@property
	def dshift(self):
		"""dshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dshift'):
			from .Satellite_.Dshift import Dshift
			self._dshift = Dshift(self._core, self._base)
		return self._dshift

	@property
	def elevation(self):
		"""elevation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_elevation'):
			from .Satellite_.Elevation import Elevation
			self._elevation = Elevation(self._core, self._base)
		return self._elevation

	@property
	def idelay(self):
		"""idelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_idelay'):
			from .Satellite_.Idelay import Idelay
			self._idelay = Idelay(self._core, self._base)
		return self._idelay

	@property
	def position(self):
		"""position commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_position'):
			from .Satellite_.Position import Position
			self._position = Position(self._core, self._base)
		return self._position

	@property
	def prange(self):
		"""prange commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prange'):
			from .Satellite_.Prange import Prange
			self._prange = Prange(self._core, self._base)
		return self._prange

	@property
	def prbRate(self):
		"""prbRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbRate'):
			from .Satellite_.PrbRate import PrbRate
			self._prbRate = PrbRate(self._core, self._base)
		return self._prbRate

	@property
	def prBias(self):
		"""prBias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prBias'):
			from .Satellite_.PrBias import PrBias
			self._prBias = PrBias(self._core, self._base)
		return self._prBias

	@property
	def prRate(self):
		"""prRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prRate'):
			from .Satellite_.PrRate import PrRate
			self._prRate = PrRate(self._core, self._base)
		return self._prRate

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_range'):
			from .Satellite_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range

	@property
	def rrate(self):
		"""rrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rrate'):
			from .Satellite_.Rrate import Rrate
			self._rrate = Rrate(self._core, self._base)
		return self._rrate

	@property
	def select(self):
		"""select commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_select'):
			from .Satellite_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	@property
	def slevel(self):
		"""slevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slevel'):
			from .Satellite_.Slevel import Slevel
			self._slevel = Slevel(self._core, self._base)
		return self._slevel

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Satellite_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Satellite_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Satellite_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	@property
	def velocity(self):
		"""velocity commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_velocity'):
			from .Satellite_.Velocity import Velocity
			self._velocity = Velocity(self._core, self._base)
		return self._velocity

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.LogFmtSat:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:SATellite:FORMat \n
		Sets the file format in that the logged data is stored. \n
			:return: format_py: CSV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:SATellite:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.LogFmtSat)
