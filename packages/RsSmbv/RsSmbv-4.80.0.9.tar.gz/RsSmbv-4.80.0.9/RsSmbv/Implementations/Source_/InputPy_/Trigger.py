from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SlopeType:
		"""[SOURce]:INPut:TRIGger:SLOPe \n
		Sets the polarity of the active slope of an applied instrument trigger. \n
			:return: slope: NEGative| POSitive
		"""
		response = self._core.io.query_str('SOURce:INPut:TRIGger:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)

	def set_slope(self, slope: enums.SlopeType) -> None:
		"""[SOURce]:INPut:TRIGger:SLOPe \n
		Sets the polarity of the active slope of an applied instrument trigger. \n
			:param slope: NEGative| POSitive
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SlopeType)
		self._core.io.write(f'SOURce:INPut:TRIGger:SLOPe {param}')
