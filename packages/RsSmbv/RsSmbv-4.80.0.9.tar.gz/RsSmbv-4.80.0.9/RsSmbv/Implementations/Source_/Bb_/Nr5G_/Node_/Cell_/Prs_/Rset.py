from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rset:
	"""Rset commands group definition. 18 total commands, 9 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rset", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Rset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rset(self._core, self._base.parent)
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
	def cmbSize(self):
		"""cmbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmbSize'):
			from .Rset_.CmbSize import CmbSize
			self._cmbSize = CmbSize(self._core, self._base)
		return self._cmbSize

	@property
	def nresources(self):
		"""nresources commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nresources'):
			from .Rset_.Nresources import Nresources
			self._nresources = Nresources(self._core, self._base)
		return self._nresources

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .Rset_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .Rset_.RbNumber import RbNumber
			self._rbNumber = RbNumber(self._core, self._base)
		return self._rbNumber

	@property
	def rbStart(self):
		"""rbStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbStart'):
			from .Rset_.RbStart import RbStart
			self._rbStart = RbStart(self._core, self._base)
		return self._rbStart

	@property
	def repFactor(self):
		"""repFactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repFactor'):
			from .Rset_.RepFactor import RepFactor
			self._repFactor = RepFactor(self._core, self._base)
		return self._repFactor

	@property
	def res(self):
		"""res commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_res'):
			from .Rset_.Res import Res
			self._res = Res(self._core, self._base)
		return self._res

	@property
	def slOffset(self):
		"""slOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slOffset'):
			from .Rset_.SlOffset import SlOffset
			self._slOffset = SlOffset(self._core, self._base)
		return self._slOffset

	@property
	def tgap(self):
		"""tgap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgap'):
			from .Rset_.Tgap import Tgap
			self._tgap = Tgap(self._core, self._base)
		return self._tgap
