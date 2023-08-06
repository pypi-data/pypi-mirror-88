from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandwidth", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AutoManualMode:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE \n
		For method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.modeQHIG|QHT, sets how the signal bandwidth is estimated:
		automatically or manually with the command CORRection:FRESponse:RF:OPTimization. \n
			:return: freq_resp_opt_bw_mo: AUTO| MANual
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_mode(self, freq_resp_opt_bw_mo: enums.AutoManualMode) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE \n
		For method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.modeQHIG|QHT, sets how the signal bandwidth is estimated:
		automatically or manually with the command CORRection:FRESponse:RF:OPTimization. \n
			:param freq_resp_opt_bw_mo: AUTO| MANual
		"""
		param = Conversions.enum_scalar_to_str(freq_resp_opt_bw_mo, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE {param}')

	def get_value(self) -> int:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:[VALue] \n
		Sets the signal compensation bandwidth for method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.Bandwidth.mode MAN. \n
			:return: freq_resp_opt_bw_va: integer Range: depends on installed baseband extension option * e.g. for base unit without extensions max = 120 MHz For more information, see data sheet.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:VALue?')
		return Conversions.str_to_int(response)

	def set_value(self, freq_resp_opt_bw_va: int) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:[VALue] \n
		Sets the signal compensation bandwidth for method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.Bandwidth.mode MAN. \n
			:param freq_resp_opt_bw_va: integer Range: depends on installed baseband extension option * e.g. for base unit without extensions max = 120 MHz For more information, see data sheet.
		"""
		param = Conversions.decimal_value_to_str(freq_resp_opt_bw_va)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:VALue {param}')
