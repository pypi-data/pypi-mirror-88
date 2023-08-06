from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ModulationDevMode:
		"""[SOURce<HW>]:AM:DEViation:MODE \n
		Selects the coupling mode. The coupling mode parameter also determines the mode for fixing the total depth. \n
			:return: am_dev_mode: UNCoupled| TOTal| RATio UNCoupled Does not couple the LF signals. The deviation depth values of both paths are independent. TOTal Couples the deviation depth of both paths. RATio Couples the deviation depth ratio of both paths
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AM:DEViation:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationDevMode)

	def set_mode(self, am_dev_mode: enums.ModulationDevMode) -> None:
		"""[SOURce<HW>]:AM:DEViation:MODE \n
		Selects the coupling mode. The coupling mode parameter also determines the mode for fixing the total depth. \n
			:param am_dev_mode: UNCoupled| TOTal| RATio UNCoupled Does not couple the LF signals. The deviation depth values of both paths are independent. TOTal Couples the deviation depth of both paths. RATio Couples the deviation depth ratio of both paths
		"""
		param = Conversions.enum_scalar_to_str(am_dev_mode, enums.ModulationDevMode)
		self._core.io.write(f'SOURce<HwInstance>:AM:DEViation:MODE {param}')
