from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpd:
	"""Dpd commands group definition. 49 total commands, 13 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpd", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Dpd':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpd(self._core, self._base.parent)
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
		"""amam commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_amam'):
			from .Dpd_.Amam import Amam
			self._amam = Amam(self._core, self._base)
		return self._amam

	@property
	def amFirst(self):
		"""amFirst commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amFirst'):
			from .Dpd_.AmFirst import AmFirst
			self._amFirst = AmFirst(self._core, self._base)
		return self._amFirst

	@property
	def amPm(self):
		"""amPm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_amPm'):
			from .Dpd_.AmPm import AmPm
			self._amPm = AmPm(self._core, self._base)
		return self._amPm

	@property
	def gain(self):
		"""gain commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gain'):
			from .Dpd_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def inputPy(self):
		"""inputPy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .Dpd_.InputPy import InputPy
			self._inputPy = InputPy(self._core, self._base)
		return self._inputPy

	@property
	def lreference(self):
		"""lreference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lreference'):
			from .Dpd_.Lreference import Lreference
			self._lreference = Lreference(self._core, self._base)
		return self._lreference

	@property
	def measurement(self):
		"""measurement commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_measurement'):
			from .Dpd_.Measurement import Measurement
			self._measurement = Measurement(self._core, self._base)
		return self._measurement

	@property
	def output(self):
		"""output commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Dpd_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def pin(self):
		"""pin commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pin'):
			from .Dpd_.Pin import Pin
			self._pin = Pin(self._core, self._base)
		return self._pin

	@property
	def scale(self):
		"""scale commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scale'):
			from .Dpd_.Scale import Scale
			self._scale = Scale(self._core, self._base)
		return self._scale

	@property
	def setting(self):
		"""setting commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_setting'):
			from .Dpd_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def shaping(self):
		"""shaping commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_shaping'):
			from .Dpd_.Shaping import Shaping
			self._shaping = Shaping(self._core, self._base)
		return self._shaping

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dpd_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def preset(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:PRESet \n
		Sets the default DPD settings (*RST values specified for the commands) . Not affected is the state set with the command
		method RsSmbv.Source.Iq.Dpd.State.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:PRESet')

	def preset_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:IQ:DPD<ST>:PRESet \n
		Sets the default DPD settings (*RST values specified for the commands) . Not affected is the state set with the command
		method RsSmbv.Source.Iq.Dpd.State.set. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:PRESet')
