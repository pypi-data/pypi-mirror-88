from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reference", core, parent)

	# noinspection PyTypeChecker
	def get_vehicle(self) -> enums.RefVehicle:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:REFerence:VEHicle \n
		No command help available \n
			:return: reference_vehicl: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:SELection:REFerence:VEHicle?')
		return Conversions.str_to_scalar_enum(response, enums.RefVehicle)

	def set_vehicle(self, reference_vehicl: enums.RefVehicle) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:REFerence:VEHicle \n
		No command help available \n
			:param reference_vehicl: No help available
		"""
		param = Conversions.enum_scalar_to_str(reference_vehicl, enums.RefVehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:REFerence:VEHicle {param}')
