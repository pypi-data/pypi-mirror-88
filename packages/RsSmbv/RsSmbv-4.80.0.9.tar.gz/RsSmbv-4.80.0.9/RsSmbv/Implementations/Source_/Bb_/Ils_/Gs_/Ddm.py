from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ddm:
	"""Ddm commands group definition. 8 total commands, 0 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ddm", core, parent)

	# noinspection PyTypeChecker
	def get_coupling(self) -> enums.AvionicIlsDdmCoup:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:COUPling \n
		Selects if the DDM value is fixed or is changed with a change of sum of modulation depths (SDM, see SDM) . \n
			:return: coupling: FIXed| SDM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsDdmCoup)

	def set_coupling(self, coupling: enums.AvionicIlsDdmCoup) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:COUPling \n
		Selects if the DDM value is fixed or is changed with a change of sum of modulation depths (SDM, see SDM) . \n
			:param coupling: FIXed| SDM
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.AvionicIlsDdmCoup)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:COUPling {param}')

	def get_current(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:CURRent \n
		Sets the DDM value alternatively as a current by means of the ILS indicating instrument. The instrument current is
		calculated according to: DDM Current µA = DDM Depth [%] × 857,125 µA A variation of the instrument current automatically
		leads to a variation of the DDM value and the DDM value in dB. \n
			:return: current: float Range: -8.57125E-4 to 8.57125E-4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:CURRent?')
		return Conversions.str_to_float(response)

	def set_current(self, current: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:CURRent \n
		Sets the DDM value alternatively as a current by means of the ILS indicating instrument. The instrument current is
		calculated according to: DDM Current µA = DDM Depth [%] × 857,125 µA A variation of the instrument current automatically
		leads to a variation of the DDM value and the DDM value in dB. \n
			:param current: float Range: -8.57125E-4 to 8.57125E-4
		"""
		param = Conversions.decimal_value_to_str(current)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:CURRent {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.UpDownDirection:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:DIRection \n
		Sets the simulation mode for the ILS glide slope modulation signal. A change of the setting automatically changes the
		sign of the DDM value. \n
			:return: direction: UP| DOWN UP The 150 Hz modulation signal is predominant, the DDM value is negative (the airplane is too low, it must climb) . DOWN The 90 Hz modulation signal is predominant, the DDM value is positive (the airplane is too high, it must descend) .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.UpDownDirection)

	def set_direction(self, direction: enums.UpDownDirection) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:DIRection \n
		Sets the simulation mode for the ILS glide slope modulation signal. A change of the setting automatically changes the
		sign of the DDM value. \n
			:param direction: UP| DOWN UP The 150 Hz modulation signal is predominant, the DDM value is negative (the airplane is too low, it must climb) . DOWN The 90 Hz modulation signal is predominant, the DDM value is positive (the airplane is too high, it must descend) .
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.UpDownDirection)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:DIRection {param}')

	def get_logarithmic(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:LOGarithmic \n
		Sets the depth of modulation value for ILS glide slope modulation in dB.
		See also [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]. \n
			:return: logarithmic: float Range: -999.9 to 999.9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:LOGarithmic?')
		return Conversions.str_to_float(response)

	def set_logarithmic(self, logarithmic: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:LOGarithmic \n
		Sets the depth of modulation value for ILS glide slope modulation in dB.
		See also [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]. \n
			:param logarithmic: float Range: -999.9 to 999.9
		"""
		param = Conversions.decimal_value_to_str(logarithmic)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:LOGarithmic {param}')

	def get_pct(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:PCT \n
		Sets the difference in depth of modulation between the signal of the upper lobe (90 Hz) and the lower lobe (150 Hz) . The
		maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.
		See also [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]. \n
			:return: pct: float Range: -80.0 to 80.0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:PCT?')
		return Conversions.str_to_float(response)

	def set_pct(self, pct: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:PCT \n
		Sets the difference in depth of modulation between the signal of the upper lobe (90 Hz) and the lower lobe (150 Hz) . The
		maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.
		See also [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]. \n
			:param pct: float Range: -80.0 to 80.0
		"""
		param = Conversions.decimal_value_to_str(pct)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:PCT {param}')

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.AvionicIlsDdmPol:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:POLarity \n
		Sets the polarity for DDM calculation (see [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]) .
		The DDM depth calculation depends on the selected polarity:
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- Polarity 90 Hz - 150 Hz (default setting) : DDM = [ AM (90 Hz) - AM (150 Hz) ] / 100%
			- Polarity 150 Hz - 90 Hz: DDM = [ AM (150 Hz) - AM (90 Hz) ] / 100% \n
			:return: polarity: P90_150| P150_90
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsDdmPol)

	def set_polarity(self, polarity: enums.AvionicIlsDdmPol) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:POLarity \n
		Sets the polarity for DDM calculation (see [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]) .
		The DDM depth calculation depends on the selected polarity:
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- Polarity 90 Hz - 150 Hz (default setting) : DDM = [ AM (90 Hz) - AM (150 Hz) ] / 100%
			- Polarity 150 Hz - 90 Hz: DDM = [ AM (150 Hz) - AM (90 Hz) ] / 100% \n
			:param polarity: P90_150| P150_90
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.AvionicIlsDdmPol)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:POLarity {param}')

	# noinspection PyTypeChecker
	def get_step(self) -> enums.AvionicDdmStep:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:STEP \n
		Sets the variation of the difference in depth of modulation via the rotary knob. \n
			:return: ddm_step: DECimal| PREDefined
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:STEP?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDdmStep)

	def set_step(self, ddm_step: enums.AvionicDdmStep) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:STEP \n
		Sets the variation of the difference in depth of modulation via the rotary knob. \n
			:param ddm_step: DECimal| PREDefined
		"""
		param = Conversions.enum_scalar_to_str(ddm_step, enums.AvionicDdmStep)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:STEP {param}')

	def get_depth(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:[DEPTh] \n
		Sets the difference in depth of modulation between the signal of the upper/left lobe (90 Hz) and the lower/right lobe
		(150 Hz) . The maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone. The following is
		true: ILS:GS|GSL:DDM:DEPTh = (AM(90Hz) - AM(150Hz) )/100% A variation of the DDM value automatically leads to a variation
		of the DDM value in dB and the value of the instrument current. \n
			:return: depth: float Range: -0.8 to 0.8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:DDM:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:[GS]:DDM:[DEPTh] \n
		Sets the difference in depth of modulation between the signal of the upper/left lobe (90 Hz) and the lower/right lobe
		(150 Hz) . The maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone. The following is
		true: ILS:GS|GSL:DDM:DEPTh = (AM(90Hz) - AM(150Hz) )/100% A variation of the DDM value automatically leads to a variation
		of the DDM value in dB and the value of the instrument current. \n
			:param depth: float Range: -0.8 to 0.8
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:DDM:DEPTh {param}')
