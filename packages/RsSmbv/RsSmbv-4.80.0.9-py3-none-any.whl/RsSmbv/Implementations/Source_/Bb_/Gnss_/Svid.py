from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Svid:
	"""Svid commands group definition. 1253 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("svid", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Svid':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Svid(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def beidou(self):
		"""beidou commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Svid_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Svid_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Svid_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Svid_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Svid_.Navic import Navic
			self._navic = Navic(self._core, self._base)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Svid_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def sbas(self):
		"""sbas commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Svid_.Sbas import Sbas
			self._sbas = Sbas(self._core, self._base)
		return self._sbas
