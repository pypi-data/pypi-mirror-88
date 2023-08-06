from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Parameter:
	"""Parameter commands group definition. 8 total commands, 0 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("parameter", core, parent)

	def get_apco_25(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:APCO25 \n
		Sets the rolloff factor for filter type APCO25. \n
			:return: apco_25: float Range: 0.05 to 0.99
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:APCO25 \n
		Sets the rolloff factor for filter type APCO25. \n
			:param apco_25: float Range: 0.05 to 0.99
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:APCO25 {param}')

	def get_cosine(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:COSine \n
		Sets the rolloff factor for the Cosine filter type. \n
			:return: cosine: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_cosine(self, cosine: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:COSine \n
		Sets the rolloff factor for the Cosine filter type. \n
			:param cosine: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:COSine {param}')

	def get_gauss(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:GAUSs \n
		Sets the rolloff factor for the Gauss filter type. \n
			:return: gauss: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:GAUSs \n
		Sets the rolloff factor for the Gauss filter type. \n
			:param gauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:LPASSEVM \n
		Sets the cutoff frequency factor for the lowpass filter (EVM Opt.) type. \n
			:return: lpass_evm: float Range: 0.05 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, lpass_evm: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:LPASSEVM \n
		Sets the cutoff frequency factor for the lowpass filter (EVM Opt.) type. \n
			:param lpass_evm: float Range: 0.05 to 2
		"""
		param = Conversions.decimal_value_to_str(lpass_evm)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:LPASs \n
		Sets the cutoff frequency factor for the lowpass filter (ACP Opt.) type. \n
			:return: lpass: float Range: 0.05 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:LPASs \n
		Sets the cutoff frequency factor for the lowpass filter (ACP Opt.) type. \n
			:param lpass: float Range: 0.05 to 2
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:LPASs {param}')

	def get_pgauss(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:PGAuss \n
		Sets the rolloff factor for the Pure Gauss filter type. \n
			:return: pgauss: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:PGAuss?')
		return Conversions.str_to_float(response)

	def set_pgauss(self, pgauss: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:PGAuss \n
		Sets the rolloff factor for the Pure Gauss filter type. \n
			:param pgauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(pgauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:PGAuss {param}')

	def get_rcosine(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:RCOSine \n
		Sets the rolloff factor for the Root Cosine filter type. \n
			:return: rcosine: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:RCOSine \n
		Sets the rolloff factor for the Root Cosine filter type. \n
			:param rcosine: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:SPHase \n
		Sets BxT for the Split Phase filter type. \n
			:return: sphase: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:PARameter:SPHase \n
		Sets BxT for the Split Phase filter type. \n
			:param sphase: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:PARameter:SPHase {param}')
