from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Msettings:
	"""Msettings commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("msettings", core, parent)

	def get_fdeviation(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:MSETtings:FDEViation \n
		Sets the frequency deviation. \n
			:return: fdeviation: float Range: Depends on Bluetooth mode
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:MSETtings:FDEViation?')
		return Conversions.str_to_float(response)

	def set_fdeviation(self, fdeviation: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:MSETtings:FDEViation \n
		Sets the frequency deviation. \n
			:param fdeviation: float Range: Depends on Bluetooth mode
		"""
		param = Conversions.decimal_value_to_str(fdeviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:MSETtings:FDEViation {param}')
