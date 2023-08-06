from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sbas:
	"""Sbas commands group definition. 104 total commands, 13 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sbas", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Sbas':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sbas(self._core, self._base.parent)
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
	def healthy(self):
		"""healthy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_healthy'):
			from .Sbas_.Healthy import Healthy
			self._healthy = Healthy(self._core, self._base)
		return self._healthy

	@property
	def listPy(self):
		"""listPy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_listPy'):
			from .Sbas_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def mcontrol(self):
		"""mcontrol commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mcontrol'):
			from .Sbas_.Mcontrol import Mcontrol
			self._mcontrol = Mcontrol(self._core, self._base)
		return self._mcontrol

	@property
	def mpath(self):
		"""mpath commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mpath'):
			from .Sbas_.Mpath import Mpath
			self._mpath = Mpath(self._core, self._base)
		return self._mpath

	@property
	def nmessage(self):
		"""nmessage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmessage'):
			from .Sbas_.Nmessage import Nmessage
			self._nmessage = Nmessage(self._core, self._base)
		return self._nmessage

	@property
	def power(self):
		"""power commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Sbas_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def prErrors(self):
		"""prErrors commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_prErrors'):
			from .Sbas_.PrErrors import PrErrors
			self._prErrors = PrErrors(self._core, self._base)
		return self._prErrors

	@property
	def present(self):
		"""present commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_present'):
			from .Sbas_.Present import Present
			self._present = Present(self._core, self._base)
		return self._present

	@property
	def sdynamics(self):
		"""sdynamics commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_sdynamics'):
			from .Sbas_.Sdynamics import Sdynamics
			self._sdynamics = Sdynamics(self._core, self._base)
		return self._sdynamics

	@property
	def signal(self):
		"""signal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_signal'):
			from .Sbas_.Signal import Signal
			self._signal = Signal(self._core, self._base)
		return self._signal

	@property
	def simulated(self):
		"""simulated commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_simulated'):
			from .Sbas_.Simulated import Simulated
			self._simulated = Simulated(self._core, self._base)
		return self._simulated

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sbas_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def visibility(self):
		"""visibility commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_visibility'):
			from .Sbas_.Visibility import Visibility
			self._visibility = Visibility(self._core, self._base)
		return self._visibility
