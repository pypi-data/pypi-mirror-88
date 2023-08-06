from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Td:
	"""Td commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: PdschTdoAlloc, default value after init: PdschTdoAlloc.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("td", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_pdschTdoAlloc_get', 'repcap_pdschTdoAlloc_set', repcap.PdschTdoAlloc.Nr0)

	def clone(self) -> 'Td':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Td(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_pdschTdoAlloc_set(self, enum_value: repcap.PdschTdoAlloc) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PdschTdoAlloc.Default
		Default value after init: PdschTdoAlloc.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_pdschTdoAlloc_get(self) -> repcap.PdschTdoAlloc:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def knull(self):
		"""knull commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_knull'):
			from .Td_.Knull import Knull
			self._knull = Knull(self._core, self._base)
		return self._knull

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Td_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def mapping(self):
		"""mapping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapping'):
			from .Td_.Mapping import Mapping
			self._mapping = Mapping(self._core, self._base)
		return self._mapping

	@property
	def sliv(self):
		"""sliv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sliv'):
			from .Td_.Sliv import Sliv
			self._sliv = Sliv(self._core, self._base)
		return self._sliv

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Td_.Start import Start
			self._start = Start(self._core, self._base)
		return self._start
