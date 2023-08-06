from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 45 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: CarrierComponent, default value after init: CarrierComponent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_carrierComponent_get', 'repcap_carrierComponent_set', repcap.CarrierComponent.Nr1)

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_carrierComponent_set(self, enum_value: repcap.CarrierComponent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CarrierComponent.Default
		Default value after init: CarrierComponent.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_carrierComponent_get(self) -> repcap.CarrierComponent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Cell_.Poffset import Poffset
			self._poffset = Poffset(self._core, self._base)
		return self._poffset

	@property
	def eimta(self):
		"""eimta commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_eimta'):
			from .Cell_.Eimta import Eimta
			self._eimta = Eimta(self._core, self._base)
		return self._eimta

	@property
	def frc(self):
		"""frc commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .Cell_.Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def pusch(self):
		"""pusch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Cell_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	@property
	def refsig(self):
		"""refsig commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_refsig'):
			from .Cell_.Refsig import Refsig
			self._refsig = Refsig(self._core, self._base)
		return self._refsig
