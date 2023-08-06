from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gs:
	"""Gs commands group definition. 17 total commands, 5 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gs", core, parent)

	def clone(self) -> 'Gs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ddm(self):
		"""ddm commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_ddm'):
			from .Gs_.Ddm import Ddm
			self._ddm = Ddm(self._core, self._base)
		return self._ddm

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .Gs_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def icao(self):
		"""icao commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icao'):
			from .Gs_.Icao import Icao
			self._icao = Icao(self._core, self._base)
		return self._icao

	@property
	def llobe(self):
		"""llobe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_llobe'):
			from .Gs_.Llobe import Llobe
			self._llobe = Llobe(self._core, self._base)
		return self._llobe

	@property
	def ulobe(self):
		"""ulobe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulobe'):
			from .Gs_.Ulobe import Ulobe
			self._ulobe = Ulobe(self._core, self._base)
		return self._ulobe

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicIlsGsMode:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:MODE \n
		Sets the operating mode for the ILS glide slope modulation signal. \n
			:return: mode: NORM| ULOBe| LLOBe NORM ILS glide slope modulation is active. ULOBe Amplitude modulation of the output signal with the upper lobe (90Hz) signal component of the ILS glide slope signal is active. LLOBe Amplitude modulation of the output signal with the lower lobe (150Hz) signal component of the ILS glide slope signal is active.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsGsMode)

	def set_mode(self, mode: enums.AvionicIlsGsMode) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:MODE \n
		Sets the operating mode for the ILS glide slope modulation signal. \n
			:param mode: NORM| ULOBe| LLOBe NORM ILS glide slope modulation is active. ULOBe Amplitude modulation of the output signal with the upper lobe (90Hz) signal component of the ILS glide slope signal is active. LLOBe Amplitude modulation of the output signal with the lower lobe (150Hz) signal component of the ILS glide slope signal is active.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicIlsGsMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:MODE {param}')

	def get_phase(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:PHASe \n
		Sets the phase between the modulation signals of the upper and lower antenna lobe of the ILS glide slope signal.
		Zero crossing of the lower lobe (150 Hz) signal serves as a reference. The angle refers to the period of the signal of
		the right antenna lobe. \n
			:return: phase: float Range: -60 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:PHASe?')
		return Conversions.str_to_float(response)

	def set_phase(self, phase: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:PHASe \n
		Sets the phase between the modulation signals of the upper and lower antenna lobe of the ILS glide slope signal.
		Zero crossing of the lower lobe (150 Hz) signal serves as a reference. The angle refers to the period of the signal of
		the right antenna lobe. \n
			:param phase: float Range: -60 to 120
		"""
		param = Conversions.decimal_value_to_str(phase)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:PHASe {param}')

	def get_sdm(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:SDM \n
		Sets the arithmetic sum of the modulation depths of the upper lobe (90 Hz) and lower lobe (150 Hz) for the ILS glide
		slope signal contents. The RMS modulation depth of the sum signal depends on the phase setting of both modulation tones. \n
			:return: sdm: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:SDM?')
		return Conversions.str_to_float(response)

	def set_sdm(self, sdm: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:SDM \n
		Sets the arithmetic sum of the modulation depths of the upper lobe (90 Hz) and lower lobe (150 Hz) for the ILS glide
		slope signal contents. The RMS modulation depth of the sum signal depends on the phase setting of both modulation tones. \n
			:param sdm: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(sdm)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:SDM {param}')
