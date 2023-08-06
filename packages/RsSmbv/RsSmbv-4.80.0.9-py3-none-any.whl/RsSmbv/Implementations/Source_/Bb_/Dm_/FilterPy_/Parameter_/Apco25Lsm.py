from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apco25Lsm:
	"""Apco25Lsm commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apco25Lsm", core, parent)

	def get_gauss(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:APCO25Lsm:GAUSs \n
		Sets the filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / Min / Max / Increment / Default \n
			- APCO25 / Roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- APCO25Lsm / Cut off frequency for the lowpass/gauss filter (LOWPass/:GAUSs) / <Cosine> / 400 / 25E6 / 1E-3 / 270833.333
			- COSine / Bandwidth / <FiltParm> / 400 / depends on the installed options*) / 1E-3 / 270833.333
			- COSine / Roll-off factor / <Cosine> / 0.05 / 1 / 0.01 / 0.35
			- GAUSs / Roll-off factor / <Gauss> / 0.15 / 100000 / 0.01 / 0.3
			- LPASs / Cut-off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / Cut-off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / Roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / Roll-off factor / <RCosine> / 0.05 / 1 / 0.001 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2
		*) 100E6 (base unit) / 200E6 (R&S SMBVB-K523) / 300E6 (R&S SMBVB-K524) \n
			:return: gauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:APCO25Lsm:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:APCO25Lsm:GAUSs \n
		Sets the filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / Min / Max / Increment / Default \n
			- APCO25 / Roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- APCO25Lsm / Cut off frequency for the lowpass/gauss filter (LOWPass/:GAUSs) / <Cosine> / 400 / 25E6 / 1E-3 / 270833.333
			- COSine / Bandwidth / <FiltParm> / 400 / depends on the installed options*) / 1E-3 / 270833.333
			- COSine / Roll-off factor / <Cosine> / 0.05 / 1 / 0.01 / 0.35
			- GAUSs / Roll-off factor / <Gauss> / 0.15 / 100000 / 0.01 / 0.3
			- LPASs / Cut-off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / Cut-off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / Roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / Roll-off factor / <RCosine> / 0.05 / 1 / 0.001 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2
		*) 100E6 (base unit) / 200E6 (R&S SMBVB-K523) / 300E6 (R&S SMBVB-K524) \n
			:param gauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:APCO25Lsm:GAUSs {param}')

	def get_low_pass(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:APCO25Lsm:LOWPass \n
		Sets the filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / Min / Max / Increment / Default \n
			- APCO25 / Roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- APCO25Lsm / Cut off frequency for the lowpass/gauss filter (LOWPass/:GAUSs) / <Cosine> / 400 / 25E6 / 1E-3 / 270833.333
			- COSine / Bandwidth / <FiltParm> / 400 / depends on the installed options*) / 1E-3 / 270833.333
			- COSine / Roll-off factor / <Cosine> / 0.05 / 1 / 0.01 / 0.35
			- GAUSs / Roll-off factor / <Gauss> / 0.15 / 100000 / 0.01 / 0.3
			- LPASs / Cut-off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / Cut-off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / Roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / Roll-off factor / <RCosine> / 0.05 / 1 / 0.001 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2
		*) 100E6 (base unit) / 200E6 (R&S SMBVB-K523) / 300E6 (R&S SMBVB-K524) \n
			:return: filt_parm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:APCO25Lsm:LOWPass?')
		return Conversions.str_to_float(response)

	def set_low_pass(self, filt_parm: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:APCO25Lsm:LOWPass \n
		Sets the filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / Min / Max / Increment / Default \n
			- APCO25 / Roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- APCO25Lsm / Cut off frequency for the lowpass/gauss filter (LOWPass/:GAUSs) / <Cosine> / 400 / 25E6 / 1E-3 / 270833.333
			- COSine / Bandwidth / <FiltParm> / 400 / depends on the installed options*) / 1E-3 / 270833.333
			- COSine / Roll-off factor / <Cosine> / 0.05 / 1 / 0.01 / 0.35
			- GAUSs / Roll-off factor / <Gauss> / 0.15 / 100000 / 0.01 / 0.3
			- LPASs / Cut-off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / Cut-off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / Roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / Roll-off factor / <RCosine> / 0.05 / 1 / 0.001 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2
		*) 100E6 (base unit) / 200E6 (R&S SMBVB-K523) / 300E6 (R&S SMBVB-K524) \n
			:param filt_parm: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(filt_parm)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:APCO25Lsm:LOWPass {param}')
