from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arbitrary:
	"""Arbitrary commands group definition. 130 total commands, 9 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arbitrary", core, parent)

	def clone(self) -> 'Arbitrary':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Arbitrary(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cfr(self):
		"""cfr commands group. 2 Sub-classes, 12 commands."""
		if not hasattr(self, '_cfr'):
			from .Arbitrary_.Cfr import Cfr
			self._cfr = Cfr(self._core, self._base)
		return self._cfr

	@property
	def clock(self):
		"""clock commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Arbitrary_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def mcarrier(self):
		"""mcarrier commands group. 9 Sub-classes, 4 commands."""
		if not hasattr(self, '_mcarrier'):
			from .Arbitrary_.Mcarrier import Mcarrier
			self._mcarrier = Mcarrier(self._core, self._base)
		return self._mcarrier

	@property
	def pramp(self):
		"""pramp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pramp'):
			from .Arbitrary_.Pramp import Pramp
			self._pramp = Pramp(self._core, self._base)
		return self._pramp

	@property
	def signal(self):
		"""signal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_signal'):
			from .Arbitrary_.Signal import Signal
			self._signal = Signal(self._core, self._base)
		return self._signal

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 6 commands."""
		if not hasattr(self, '_trigger'):
			from .Arbitrary_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def tsignal(self):
		"""tsignal commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsignal'):
			from .Arbitrary_.Tsignal import Tsignal
			self._tsignal = Tsignal(self._core, self._base)
		return self._tsignal

	@property
	def waveform(self):
		"""waveform commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_waveform'):
			from .Arbitrary_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	@property
	def wsegment(self):
		"""wsegment commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_wsegment'):
			from .Arbitrary_.Wsegment import Wsegment
			self._wsegment = Wsegment(self._core, self._base)
		return self._wsegment

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:PRESet \n
		Sets all ARB generator parameters to their default values. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:PRESet \n
		Sets all ARB generator parameters to their default values. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:ARBitrary:STATe \n
		Enables the ARB generator. A waveform must be selected before the ARB generator is activated. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:STATe \n
		Enables the ARB generator. A waveform must be selected before the ARB generator is activated. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:STATe {param}')
