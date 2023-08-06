from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digital:
	"""Digital commands group definition. 8 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("digital", core, parent)

	def clone(self) -> 'Digital':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Digital(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def iqRatio(self):
		"""iqRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqRatio'):
			from .Digital_.IqRatio import IqRatio
			self._iqRatio = IqRatio(self._core, self._base)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_leakage'):
			from .Digital_.Leakage import Leakage
			self._leakage = Leakage(self._core, self._base)
		return self._leakage

	@property
	def quadrature(self):
		"""quadrature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_quadrature'):
			from .Digital_.Quadrature import Quadrature
			self._quadrature = Quadrature(self._core, self._base)
		return self._quadrature

	def get_delay(self) -> float:
		"""[SOURce]:BB:IMPairment:DIGital:DELay \n
		Defines the time delay of both I and Q vectors between the marker signal at the marker outputs relative to the signal
		generation start. A positive value means that the I and Q vectors delay relative to the marker/trigger and vice versa.
		Value range
			Table Header: Output / Min / Max / Resolution \n
			- RF<ch> / 0 / 10E-6 / 1E-12
			- IQOutput<ch> / 500E-9 / 500E-9 / 1E-12
			- DIGital / 500E-9 / 500E-9 / 1E-12 \n
			:return: delay: float Range: 0 to 10E-6
		"""
		response = self._core.io.query_str('SOURce:BB:IMPairment:DIGital:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce]:BB:IMPairment:DIGital:DELay \n
		Defines the time delay of both I and Q vectors between the marker signal at the marker outputs relative to the signal
		generation start. A positive value means that the I and Q vectors delay relative to the marker/trigger and vice versa.
		Value range
			Table Header: Output / Min / Max / Resolution \n
			- RF<ch> / 0 / 10E-6 / 1E-12
			- IQOutput<ch> / 500E-9 / 500E-9 / 1E-12
			- DIGital / 500E-9 / 500E-9 / 1E-12 \n
			:param delay: float Range: 0 to 10E-6
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce:BB:IMPairment:DIGital:DELay {param}')

	def get_poffset(self) -> float:
		"""[SOURce]:BB:IMPairment:DIGital:POFFset \n
		Adds an additional phase offset after the stream mapper.
			INTRO_CMD_HELP: You can shift the phase at the different stages in the signal generation flow, see: \n
			- method RsSmbv.Source.Bb.poffset \n
			:return: phase_offset: float Range: -999.99 to 999.99
		"""
		response = self._core.io.query_str('SOURce:BB:IMPairment:DIGital:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, phase_offset: float) -> None:
		"""[SOURce]:BB:IMPairment:DIGital:POFFset \n
		Adds an additional phase offset after the stream mapper.
			INTRO_CMD_HELP: You can shift the phase at the different stages in the signal generation flow, see: \n
			- method RsSmbv.Source.Bb.poffset \n
			:param phase_offset: float Range: -999.99 to 999.99
		"""
		param = Conversions.decimal_value_to_str(phase_offset)
		self._core.io.write(f'SOURce:BB:IMPairment:DIGital:POFFset {param}')

	def get_skew(self) -> float:
		"""[SOURce]:BB:IMPairment:DIGital:SKEW \n
		Sets a delay between the Q vector and the I vector of the corresponding stream. \n
			:return: skew: float Range: -500E-9 to 500E-9
		"""
		response = self._core.io.query_str('SOURce:BB:IMPairment:DIGital:SKEW?')
		return Conversions.str_to_float(response)

	def set_skew(self, skew: float) -> None:
		"""[SOURce]:BB:IMPairment:DIGital:SKEW \n
		Sets a delay between the Q vector and the I vector of the corresponding stream. \n
			:param skew: float Range: -500E-9 to 500E-9
		"""
		param = Conversions.decimal_value_to_str(skew)
		self._core.io.write(f'SOURce:BB:IMPairment:DIGital:SKEW {param}')

	def get_state(self) -> bool:
		"""[SOURce]:BB:IMPairment:DIGital:STATe \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce:BB:IMPairment:DIGital:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce]:BB:IMPairment:DIGital:STATe \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:BB:IMPairment:DIGital:STATe {param}')
