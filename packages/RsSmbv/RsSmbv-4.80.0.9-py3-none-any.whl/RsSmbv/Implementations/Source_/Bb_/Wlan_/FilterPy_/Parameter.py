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
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:APCO25 \n
		No command help available \n
			:return: apco_25: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:APCO25 \n
		No command help available \n
			:param apco_25: No help available
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:APCO25 {param}')

	def get_cosine(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:COSine \n
		No command help available \n
			:return: cosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_cosine(self, cosine: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:COSine \n
		No command help available \n
			:param cosine: No help available
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:COSine {param}')

	def get_gauss(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:GAUSs \n
		No command help available \n
			:return: gauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:GAUSs \n
		No command help available \n
			:param gauss: No help available
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:LPASSEVM \n
		No command help available \n
			:return: lpassevm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, lpassevm: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:LPASSEVM \n
		No command help available \n
			:param lpassevm: No help available
		"""
		param = Conversions.decimal_value_to_str(lpassevm)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:LPASs \n
		No command help available \n
			:return: lpass: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:LPASs \n
		No command help available \n
			:param lpass: No help available
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:LPASs {param}')

	def get_pgauss(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:PGAuss \n
		No command help available \n
			:return: pgauss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:PGAuss?')
		return Conversions.str_to_float(response)

	def set_pgauss(self, pgauss: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:PGAuss \n
		No command help available \n
			:param pgauss: No help available
		"""
		param = Conversions.decimal_value_to_str(pgauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:PGAuss {param}')

	def get_rcosine(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:RCOSine \n
		No command help available \n
			:return: rcosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:RCOSine \n
		No command help available \n
			:param rcosine: No help available
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:SPHase \n
		No command help available \n
			:return: sphase: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:FILTer:PARameter:SPHase \n
		No command help available \n
			:param sphase: No help available
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FILTer:PARameter:SPHase {param}')
