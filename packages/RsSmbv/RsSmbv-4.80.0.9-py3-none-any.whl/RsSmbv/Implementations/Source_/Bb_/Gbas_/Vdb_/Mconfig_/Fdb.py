from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdb:
	"""Fdb commands group definition. 15 total commands, 10 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fdb", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Fdb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fdb(self._core, self._base.parent)
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
	def aid(self):
		"""aid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aid'):
			from .Fdb_.Aid import Aid
			self._aid = Aid(self._core, self._base)
		return self._aid

	@property
	def atcHeight(self):
		"""atcHeight commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atcHeight'):
			from .Fdb_.AtcHeight import AtcHeight
			self._atcHeight = AtcHeight(self._core, self._base)
		return self._atcHeight

	@property
	def ddlocation(self):
		"""ddlocation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ddlocation'):
			from .Fdb_.Ddlocation import Ddlocation
			self._ddlocation = Ddlocation(self._core, self._base)
		return self._ddlocation

	@property
	def dpLocation(self):
		"""dpLocation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpLocation'):
			from .Fdb_.DpLocation import DpLocation
			self._dpLocation = DpLocation(self._core, self._base)
		return self._dpLocation

	@property
	def gpAngle(self):
		"""gpAngle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gpAngle'):
			from .Fdb_.GpAngle import GpAngle
			self._gpAngle = GpAngle(self._core, self._base)
		return self._gpAngle

	@property
	def rletter(self):
		"""rletter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rletter'):
			from .Fdb_.Rletter import Rletter
			self._rletter = Rletter(self._core, self._base)
		return self._rletter

	@property
	def rnumber(self):
		"""rnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rnumber'):
			from .Fdb_.Rnumber import Rnumber
			self._rnumber = Rnumber(self._core, self._base)
		return self._rnumber

	@property
	def rpdf(self):
		"""rpdf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpdf'):
			from .Fdb_.Rpdf import Rpdf
			self._rpdf = Rpdf(self._core, self._base)
		return self._rpdf

	@property
	def rpif(self):
		"""rpif commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpif'):
			from .Fdb_.Rpif import Rpif
			self._rpif = Rpif(self._core, self._base)
		return self._rpif

	@property
	def ruIndicator(self):
		"""ruIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruIndicator'):
			from .Fdb_.RuIndicator import RuIndicator
			self._ruIndicator = RuIndicator(self._core, self._base)
		return self._ruIndicator
