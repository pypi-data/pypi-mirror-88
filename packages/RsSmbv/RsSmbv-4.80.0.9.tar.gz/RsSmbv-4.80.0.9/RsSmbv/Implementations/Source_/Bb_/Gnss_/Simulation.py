from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Simulation:
	"""Simulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("simulation", core, parent)

	def get_info(self) -> str:
		"""[SOURce<HW>]:BB:GNSS:SIMulation:INFO \n
		Queries information on the current enabled RF bands, signals and GNSS standards. \n
			:return: sim_config_info: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SIMulation:INFO?')
		return trim_str_response(response)
