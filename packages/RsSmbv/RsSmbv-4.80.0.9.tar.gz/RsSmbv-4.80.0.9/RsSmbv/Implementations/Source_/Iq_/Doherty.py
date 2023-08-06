from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Doherty:
	"""Doherty commands group definition. 31 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("doherty", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Doherty':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Doherty(self._core, self._base.parent)
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
	def amam(self):
		"""amam commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amam'):
			from .Doherty_.Amam import Amam
			self._amam = Amam(self._core, self._base)
		return self._amam

	@property
	def amPm(self):
		"""amPm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amPm'):
			from .Doherty_.AmPm import AmPm
			self._amPm = AmPm(self._core, self._base)
		return self._amPm

	@property
	def inputPy(self):
		"""inputPy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .Doherty_.InputPy import InputPy
			self._inputPy = InputPy(self._core, self._base)
		return self._inputPy

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Doherty_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def pin(self):
		"""pin commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pin'):
			from .Doherty_.Pin import Pin
			self._pin = Pin(self._core, self._base)
		return self._pin

	@property
	def scale(self):
		"""scale commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scale'):
			from .Doherty_.Scale import Scale
			self._scale = Scale(self._core, self._base)
		return self._scale

	@property
	def shaping(self):
		"""shaping commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_shaping'):
			from .Doherty_.Shaping import Shaping
			self._shaping = Shaping(self._core, self._base)
		return self._shaping
