from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gps:
	"""Gps commands group definition. 16 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gps", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Gps':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gps(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def coordinates(self):
		"""coordinates commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_coordinates'):
			from .Gps_.Coordinates import Coordinates
			self._coordinates = Coordinates(self._core, self._base)
		return self._coordinates

	@property
	def location(self):
		"""location commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_location'):
			from .Gps_.Location import Location
			self._location = Location(self._core, self._base)
		return self._location

	@property
	def svid(self):
		"""svid commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_svid'):
			from .Gps_.Svid import Svid
			self._svid = Svid(self._core, self._base)
		return self._svid

	@property
	def synchronize(self):
		"""synchronize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronize'):
			from .Gps_.Synchronize import Synchronize
			self._synchronize = Synchronize(self._core, self._base)
		return self._synchronize

	@property
	def toaData(self):
		"""toaData commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_toaData'):
			from .Gps_.ToaData import ToaData
			self._toaData = ToaData(self._core, self._base)
		return self._toaData
