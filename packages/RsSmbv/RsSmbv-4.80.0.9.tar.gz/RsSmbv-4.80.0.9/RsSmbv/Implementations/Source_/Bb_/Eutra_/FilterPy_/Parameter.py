from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Parameter:
	"""Parameter commands group definition. 14 total commands, 2 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("parameter", core, parent)

	def clone(self) -> 'Parameter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Parameter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cosine(self):
		"""cosine commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cosine'):
			from .Parameter_.Cosine import Cosine
			self._cosine = Cosine(self._core, self._base)
		return self._cosine

	@property
	def lte(self):
		"""lte commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_lte'):
			from .Parameter_.Lte import Lte
			self._lte = Lte(self._core, self._base)
		return self._lte

	def get_apco_25(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:APCO25 \n
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
			:return: apco_25: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:APCO25 \n
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
			:param apco_25: No help available
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:APCO25 {param}')

	def get_gauss(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:GAUSs \n
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
			:return: gauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:GAUSs \n
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
			:param gauss: No help available
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:LPASSEVM \n
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
			:return: cutoff_frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, cutoff_frequency: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:LPASSEVM \n
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
			:param cutoff_frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(cutoff_frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:LPASs \n
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
			:return: lpass: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:LPASs \n
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
			:param lpass: No help available
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:LPASs {param}')

	def get_pgauss(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:PGAuss \n
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
			:return: pgauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:PGAuss?')
		return Conversions.str_to_float(response)

	def set_pgauss(self, pgauss: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:PGAuss \n
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
			:param pgauss: No help available
		"""
		param = Conversions.decimal_value_to_str(pgauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:PGAuss {param}')

	def get_rcosine(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:RCOSine \n
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
			:return: rcosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:RCOSine \n
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
			:param rcosine: No help available
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:SPHase \n
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
			:return: sphase: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:SPHase \n
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
			:param sphase: No help available
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:SPHase {param}')

	def get_user(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:USER \n
		Loads the file from the default or the specified directory. Loaded are files with extension *.vaf or *.dat.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string Complete file path incl. filename and extension
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:USER?')
		return trim_str_response(response)

	def set_user(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:FILTer:PARameter:USER \n
		Loads the file from the default or the specified directory. Loaded are files with extension *.vaf or *.dat.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Complete file path incl. filename and extension
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:PARameter:USER {param}')
