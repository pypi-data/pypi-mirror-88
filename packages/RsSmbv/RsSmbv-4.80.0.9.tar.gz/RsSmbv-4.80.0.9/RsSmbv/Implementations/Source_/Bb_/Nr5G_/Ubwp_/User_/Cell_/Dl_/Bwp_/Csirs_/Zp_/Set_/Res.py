from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Res:
	"""Res commands group definition. 11 total commands, 11 Sub-groups, 0 group commands
	Repeated Capability: SrsRsrcSetRsrc, default value after init: SrsRsrcSetRsrc.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("res", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_srsRsrcSetRsrc_get', 'repcap_srsRsrcSetRsrc_set', repcap.SrsRsrcSetRsrc.Nr0)

	def clone(self) -> 'Res':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Res(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_srsRsrcSetRsrc_set(self, enum_value: repcap.SrsRsrcSetRsrc) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SrsRsrcSetRsrc.Default
		Default value after init: SrsRsrcSetRsrc.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_srsRsrcSetRsrc_get(self) -> repcap.SrsRsrcSetRsrc:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def bitmap(self):
		"""bitmap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitmap'):
			from .Res_.Bitmap import Bitmap
			self._bitmap = Bitmap(self._core, self._base)
		return self._bitmap

	@property
	def cdmType(self):
		"""cdmType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdmType'):
			from .Res_.CdmType import CdmType
			self._cdmType = CdmType(self._core, self._base)
		return self._cdmType

	@property
	def density(self):
		"""density commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_density'):
			from .Res_.Density import Density
			self._density = Density(self._core, self._base)
		return self._density

	@property
	def i0(self):
		"""i0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i0'):
			from .Res_.I0 import I0
			self._i0 = I0(self._core, self._base)
		return self._i0

	@property
	def i1(self):
		"""i1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i1'):
			from .Res_.I1 import I1
			self._i1 = I1(self._core, self._base)
		return self._i1

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Res_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .Res_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .Res_.Ports import Ports
			self._ports = Ports(self._core, self._base)
		return self._ports

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .Res_.RbNumber import RbNumber
			self._rbNumber = RbNumber(self._core, self._base)
		return self._rbNumber

	@property
	def row(self):
		"""row commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_row'):
			from .Res_.Row import Row
			self._row = Row(self._core, self._base)
		return self._row

	@property
	def srbNumber(self):
		"""srbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srbNumber'):
			from .Res_.SrbNumber import SrbNumber
			self._srbNumber = SrbNumber(self._core, self._base)
		return self._srbNumber
