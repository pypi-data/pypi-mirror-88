from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Navigation:
	"""Navigation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("navigation", core, parent)

	def get_create(self) -> str:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:NAVigation:CREate \n
		Stores the current assistance data settings into the selected navigation file. Assistance data settings are stored as
		navigation file with the specific file extensions *.rs_nav or into RINEX files with extension .10n. Refer to 'MMEMory
		Subsystem' for general information on file handling in the default and in a specific directory. \n
			:return: filename: string Filename or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:NAVigation:CREate?')
		return trim_str_response(response)

	def set_create(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:NAVigation:CREate \n
		Stores the current assistance data settings into the selected navigation file. Assistance data settings are stored as
		navigation file with the specific file extensions *.rs_nav or into RINEX files with extension .10n. Refer to 'MMEMory
		Subsystem' for general information on file handling in the default and in a specific directory. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:NAVigation:CREate {param}')

	# noinspection PyTypeChecker
	def get_dformat(self) -> enums.NavDataFormat:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:NAVigation:DFORmat \n
		Sets format of the generated navigation data file. \n
			:return: data_format: LNAV| CNAV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:NAVigation:DFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.NavDataFormat)

	def set_dformat(self, data_format: enums.NavDataFormat) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:NAVigation:DFORmat \n
		Sets format of the generated navigation data file. \n
			:param data_format: LNAV| CNAV
		"""
		param = Conversions.enum_scalar_to_str(data_format, enums.NavDataFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:NAVigation:DFORmat {param}')
