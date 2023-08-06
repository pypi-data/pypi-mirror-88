from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Parameter:
	"""Parameter commands group definition. 11 total commands, 2 Sub-groups, 7 group commands"""

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
	def apco25Lsm(self):
		"""apco25Lsm commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_apco25Lsm'):
			from .Parameter_.Apco25Lsm import Apco25Lsm
			self._apco25Lsm = Apco25Lsm(self._core, self._base)
		return self._apco25Lsm

	@property
	def cosine(self):
		"""cosine commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cosine'):
			from .Parameter_.Cosine import Cosine
			self._cosine = Cosine(self._core, self._base)
		return self._cosine

	def get_apco_25(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:APCO25 \n
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
			:return: apco_25: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:APCO25 \n
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
			:param apco_25: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:APCO25 {param}')

	def get_gauss(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:GAUSs \n
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
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:GAUSs \n
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
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:LPASSEVM \n
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
			:return: lpass_evm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, lpass_evm: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:LPASSEVM \n
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
			:param lpass_evm: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(lpass_evm)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:LPASs \n
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
			:return: lpass: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:LPASs \n
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
			:param lpass: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:LPASs {param}')

	def get_pgauss(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:PGAuss \n
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
			:return: pgauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:PGAuss?')
		return Conversions.str_to_float(response)

	def set_pgauss(self, pgauss: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:PGAuss \n
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
			:param pgauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(pgauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:PGAuss {param}')

	def get_rcosine(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:RCOSine \n
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
			:return: rcosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:RCOSine \n
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
			:param rcosine: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:SPHase \n
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
			:return: sphase: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""[SOURce<HW>]:BB:DM:FILTer:PARameter:SPHase \n
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
			:param sphase: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FILTer:PARameter:SPHase {param}')
