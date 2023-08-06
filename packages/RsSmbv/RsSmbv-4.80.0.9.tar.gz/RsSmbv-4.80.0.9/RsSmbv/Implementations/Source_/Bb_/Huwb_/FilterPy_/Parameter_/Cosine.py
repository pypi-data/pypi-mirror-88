from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cosine:
	"""Cosine commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cosine", core, parent)

	def get_cofs(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:COSine:COFS \n
		Sets the cut-off frequency shift of the applied filter. \n
			:return: cofs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:COSine:COFS?')
		return Conversions.str_to_float(response)

	def set_cofs(self, cofs: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:COSine:COFS \n
		Sets the cut-off frequency shift of the applied filter. \n
			:param cofs: float Range: -1 to 1
		"""
		param = Conversions.decimal_value_to_str(cofs)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:COSine:COFS {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:COSine \n
		Sets the filter parameter.
			Table Header: Filter type / Parameter / Parameter name / Min / Max / Increment / Default \n
			- APCO25 / Rolloff factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- COSine / Rolloff factor / <Cosine> / 0 / 1 / 0.01 / 0.1
			- GAUSs / BxT / <Gauss> / 0.15 / 2.5 / 0.01 / 0.5
			- LPASs / Cutoff frequency / <LPass> / 0.02 / 2 / 0.01 / 0.34
			- LPASSEVM / Cutoff frequency / <CutoffFrequency> / 0.05 / 2 / 0.01 / 0.29
			- PGAuss / BxT / <PGauss> / 0.15 / 2.5 / 0.01 / 0.5
			- RCOSine / Rolloff factor / <RCosine> / 0 / 1 / 0.01 / 0.22
			- SPHase / BxT / <SPhase> / 0.15 / 2.5 / 0.01 / 2 \n
			:return: cosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_value(self, cosine: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:COSine \n
		Sets the filter parameter.
			Table Header: Filter type / Parameter / Parameter name / Min / Max / Increment / Default \n
			- APCO25 / Rolloff factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- COSine / Rolloff factor / <Cosine> / 0 / 1 / 0.01 / 0.1
			- GAUSs / BxT / <Gauss> / 0.15 / 2.5 / 0.01 / 0.5
			- LPASs / Cutoff frequency / <LPass> / 0.02 / 2 / 0.01 / 0.34
			- LPASSEVM / Cutoff frequency / <CutoffFrequency> / 0.05 / 2 / 0.01 / 0.29
			- PGAuss / BxT / <PGauss> / 0.15 / 2.5 / 0.01 / 0.5
			- RCOSine / Rolloff factor / <RCosine> / 0 / 1 / 0.01 / 0.22
			- SPHase / BxT / <SPhase> / 0.15 / 2.5 / 0.01 / 2 \n
			:param cosine: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:COSine {param}')
