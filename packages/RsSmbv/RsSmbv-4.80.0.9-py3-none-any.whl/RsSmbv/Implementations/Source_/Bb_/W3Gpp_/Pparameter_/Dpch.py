from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpch:
	"""Dpch commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpch", core, parent)

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:DPCH:COUNt \n
		Sets the number of activated DPCHs. The maximum number is the ratio of the chip rate and the symbol rate (maximum 512 at
		the lowest symbol rate of 7.5 ksps) . \n
			:return: count: integer Range: 0 to 512 (Max depends on other settings)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:PPARameter:DPCH:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:DPCH:COUNt \n
		Sets the number of activated DPCHs. The maximum number is the ratio of the chip rate and the symbol rate (maximum 512 at
		the lowest symbol rate of 7.5 ksps) . \n
			:param count: integer Range: 0 to 512 (Max depends on other settings)
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:PPARameter:DPCH:COUNt {param}')

	# noinspection PyTypeChecker
	def get_symbol_rate(self) -> enums.SymbRate:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:DPCH:SRATe \n
		This command sets the symbol rate of DPCHs. The setting takes effect only after execution of command method RsSmbv.Source.
		Bb.W3Gpp.Pparameter.Execute.set. \n
			:return: srate: D7K5| D15K| D30K| D60K| D120k| D240k| D480k| D960k
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:PPARameter:DPCH:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.SymbRate)

	def set_symbol_rate(self, srate: enums.SymbRate) -> None:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:DPCH:SRATe \n
		This command sets the symbol rate of DPCHs. The setting takes effect only after execution of command method RsSmbv.Source.
		Bb.W3Gpp.Pparameter.Execute.set. \n
			:param srate: D7K5| D15K| D30K| D60K| D120k| D240k| D480k| D960k
		"""
		param = Conversions.enum_scalar_to_str(srate, enums.SymbRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:PPARameter:DPCH:SRATe {param}')
