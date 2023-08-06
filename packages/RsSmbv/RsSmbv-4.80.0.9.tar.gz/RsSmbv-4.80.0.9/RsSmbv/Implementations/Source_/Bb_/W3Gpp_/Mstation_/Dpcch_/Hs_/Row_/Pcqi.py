from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pcqi:
	"""Pcqi commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: TwoStreams, default value after init: TwoStreams.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pcqi", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_twoStreams_get', 'repcap_twoStreams_set', repcap.TwoStreams.Nr0)

	def clone(self) -> 'Pcqi':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pcqi(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_twoStreams_set(self, enum_value: repcap.TwoStreams) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TwoStreams.Default
		Default value after init: TwoStreams.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_twoStreams_get(self) -> repcap.TwoStreams:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def cqi(self):
		"""cqi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cqi'):
			from .Pcqi_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def fromPy(self):
		"""fromPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fromPy'):
			from .Pcqi_.FromPy import FromPy
			self._fromPy = FromPy(self._core, self._base)
		return self._fromPy

	@property
	def pci(self):
		"""pci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pci'):
			from .Pcqi_.Pci import Pci
			self._pci = Pci(self._core, self._base)
		return self._pci

	@property
	def to(self):
		"""to commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_to'):
			from .Pcqi_.To import To
			self._to = To(self._core, self._base)
		return self._to

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Pcqi_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
