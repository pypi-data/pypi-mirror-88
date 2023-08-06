from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hold:
	"""Hold commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hold", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:HOLD:[STATe] \n
			INTRO_CMD_HELP: For method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.modeQHIG|QHT, retains the last calculated correction values as long as one of the following is performed: \n
			- SOURce1:CORRection:FRESponse:RF:OPTimization:HOLD:STATe 0
			- method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.Local.set \n
			:return: freq_resp_hold_sta: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:HOLD:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, freq_resp_hold_sta: bool) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:HOLD:[STATe] \n
			INTRO_CMD_HELP: For method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.modeQHIG|QHT, retains the last calculated correction values as long as one of the following is performed: \n
			- SOURce1:CORRection:FRESponse:RF:OPTimization:HOLD:STATe 0
			- method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.Local.set \n
			:param freq_resp_hold_sta: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(freq_resp_hold_sta)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:HOLD:STATe {param}')
