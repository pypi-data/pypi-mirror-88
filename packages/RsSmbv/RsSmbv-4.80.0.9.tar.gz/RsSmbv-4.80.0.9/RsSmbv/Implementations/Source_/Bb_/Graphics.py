from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Graphics:
	"""Graphics commands group definition. 9 total commands, 2 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("graphics", core, parent)

	def clone(self) -> 'Graphics':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Graphics(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Graphics_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Graphics_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def set_add(self, size: enums.TranRecSize) -> None:
		"""[SOURce]:BB:GRAPhics:ADD \n
		Adds a graphical signal display (according to the current MODE, SOURce, SRATe:* and TRIGger:* settings) . \n
			:param size: MAXimized| MINimized
		"""
		param = Conversions.enum_scalar_to_str(size, enums.TranRecSize)
		self._core.io.write(f'SOURce:BB:GRAPhics:ADD {param}')

	def close(self) -> None:
		"""[SOURce]:BB:GRAPhics:CLOSe \n
		Closes all graphical signal displays. \n
		"""
		self._core.io.write(f'SOURce:BB:GRAPhics:CLOSe')

	def close_with_opc(self) -> None:
		"""[SOURce]:BB:GRAPhics:CLOSe \n
		Closes all graphical signal displays. \n
		Same as close, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce:BB:GRAPhics:CLOSe')

	def get_fft_fscale(self) -> bool:
		"""[SOURce]:BB:GRAPhics:FFTFscale \n
		Defines the normalization of the power values in the power spectrum diagram. \n
			:return: state: 0| 1| OFF| ON 1 Normalized power in dBFS 0 Shows power distribution in dB/Hz
		"""
		response = self._core.io.query_str('SOURce:BB:GRAPhics:FFTFscale?')
		return Conversions.str_to_bool(response)

	def set_fft_fscale(self, state: bool) -> None:
		"""[SOURce]:BB:GRAPhics:FFTFscale \n
		Defines the normalization of the power values in the power spectrum diagram. \n
			:param state: 0| 1| OFF| ON 1 Normalized power in dBFS 0 Shows power distribution in dB/Hz
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:BB:GRAPhics:FFTFscale {param}')

	# noinspection PyTypeChecker
	def get_fft_len(self) -> enums.TranRecFftLen:
		"""[SOURce]:BB:GRAPhics:FFTLen \n
		Sets the FFT size. \n
			:return: mode: LEN256| LEN512| LEN1024| LEN2048| LEN4096
		"""
		response = self._core.io.query_str('SOURce:BB:GRAPhics:FFTLen?')
		return Conversions.str_to_scalar_enum(response, enums.TranRecFftLen)

	def set_fft_len(self, mode: enums.TranRecFftLen) -> None:
		"""[SOURce]:BB:GRAPhics:FFTLen \n
		Sets the FFT size. \n
			:param mode: LEN256| LEN512| LEN1024| LEN2048| LEN4096
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.TranRecFftLen)
		self._core.io.write(f'SOURce:BB:GRAPhics:FFTLen {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.TranRecMode:
		"""[SOURce<HW>]:BB:GRAPhics:MODE \n
		Selects the graphics mode of the graphical signal display. \n
			:return: mode: IQ| VECTor| CCDF| PSPectrum| CONStellation| EYEI| EYEQ
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GRAPhics:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TranRecMode)

	def set_mode(self, mode: enums.TranRecMode) -> None:
		"""[SOURce<HW>]:BB:GRAPhics:MODE \n
		Selects the graphics mode of the graphical signal display. \n
			:param mode: IQ| VECTor| CCDF| PSPectrum| CONStellation| EYEI| EYEQ
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.TranRecMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GRAPhics:MODE {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TranRecSour:
		"""[SOURce]:BB:GRAPhics:SOURce \n
		Defines the signal acquisition point, that is the location in the signal flow where the displayed signal is tapped from.
		See 'Signal Acquisition Points'. \n
			:return: source: STRA| BBA| RFA| BBIA| IQO1 | DO1 STRA Stream A; input stream of the 'IQ Stream Mapper' BBA Baseband signal BBIA Digital baseband input signals RFA RF signal IQO1 Analog I/Q output signal DO1 Digital I/Q output signals; outputs of the 'IQ Stream Mapper'
		"""
		response = self._core.io.query_str('SOURce:BB:GRAPhics:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TranRecSour)

	def set_source(self, source: enums.TranRecSour) -> None:
		"""[SOURce]:BB:GRAPhics:SOURce \n
		Defines the signal acquisition point, that is the location in the signal flow where the displayed signal is tapped from.
		See 'Signal Acquisition Points'. \n
			:param source: STRA| BBA| RFA| BBIA| IQO1 | DO1 STRA Stream A; input stream of the 'IQ Stream Mapper' BBA Baseband signal BBIA Digital baseband input signals RFA RF signal IQO1 Analog I/Q output signal DO1 Digital I/Q output signals; outputs of the 'IQ Stream Mapper'
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TranRecSour)
		self._core.io.write(f'SOURce:BB:GRAPhics:SOURce {param}')
