from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DcChannel:
	"""DcChannel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcChannel", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:DCCHannel:[STATe] \n
		Activates/deactivates the dedicated control channel. F-DCCH cannot be selected for RC1 and RC2. The setting takes effect
		only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. It is specific for the selected radio
		configuration. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:DCCHannel:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:DCCHannel:[STATe] \n
		Activates/deactivates the dedicated control channel. F-DCCH cannot be selected for RC1 and RC2. The setting takes effect
		only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. It is specific for the selected radio
		configuration. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:DCCHannel:STATe {param}')
