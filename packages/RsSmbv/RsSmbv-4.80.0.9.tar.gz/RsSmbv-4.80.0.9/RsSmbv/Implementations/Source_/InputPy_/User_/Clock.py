from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.ImpG50G1KcoerceG10K:
		"""[SOURce]:INPut:USER:CLOCk:IMPedance \n
		Selects the input impedance for the external trigger inputs. \n
			:return: impedance: G1K| G50
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:CLOCk:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.ImpG50G1KcoerceG10K)

	def set_impedance(self, impedance: enums.ImpG50G1KcoerceG10K) -> None:
		"""[SOURce]:INPut:USER:CLOCk:IMPedance \n
		Selects the input impedance for the external trigger inputs. \n
			:param impedance: G1K| G50
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.ImpG50G1KcoerceG10K)
		self._core.io.write(f'SOURce:INPut:USER:CLOCk:IMPedance {param}')

	def get_level(self) -> float:
		"""[SOURce]:INPut:USER:CLOCk:LEVel \n
		Sets the threshold for any input signal at the User1-2 connectors. \n
			:return: level: float Range: 0.1 to 2
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:CLOCk:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""[SOURce]:INPut:USER:CLOCk:LEVel \n
		Sets the threshold for any input signal at the User1-2 connectors. \n
			:param level: float Range: 0.1 to 2
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:INPut:USER:CLOCk:LEVel {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SlopeType:
		"""[SOURce]:INPut:USER:CLOCk:SLOPe \n
		Sets the polarity of the active slope of an externally applied clock signal. \n
			:return: slope: NEGative| POSitive
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:CLOCk:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)

	def set_slope(self, slope: enums.SlopeType) -> None:
		"""[SOURce]:INPut:USER:CLOCk:SLOPe \n
		Sets the polarity of the active slope of an externally applied clock signal. \n
			:param slope: NEGative| POSitive
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SlopeType)
		self._core.io.write(f'SOURce:INPut:USER:CLOCk:SLOPe {param}')
