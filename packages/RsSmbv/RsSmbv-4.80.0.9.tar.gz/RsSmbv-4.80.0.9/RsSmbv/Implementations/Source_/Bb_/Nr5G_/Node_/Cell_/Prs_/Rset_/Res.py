from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Res:
	"""Res commands group definition. 10 total commands, 7 Sub-groups, 0 group commands
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
	def apMap(self):
		"""apMap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apMap'):
			from .Res_.ApMap import ApMap
			self._apMap = ApMap(self._core, self._base)
		return self._apMap

	@property
	def nsymbol(self):
		"""nsymbol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsymbol'):
			from .Res_.Nsymbol import Nsymbol
			self._nsymbol = Nsymbol(self._core, self._base)
		return self._nsymbol

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Res_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def reOffset(self):
		"""reOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reOffset'):
			from .Res_.ReOffset import ReOffset
			self._reOffset = ReOffset(self._core, self._base)
		return self._reOffset

	@property
	def slOffset(self):
		"""slOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slOffset'):
			from .Res_.SlOffset import SlOffset
			self._slOffset = SlOffset(self._core, self._base)
		return self._slOffset

	@property
	def sqid(self):
		"""sqid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sqid'):
			from .Res_.Sqid import Sqid
			self._sqid = Sqid(self._core, self._base)
		return self._sqid

	@property
	def syOffset(self):
		"""syOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_syOffset'):
			from .Res_.SyOffset import SyOffset
			self._syOffset = SyOffset(self._core, self._base)
		return self._syOffset
