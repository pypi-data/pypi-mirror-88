from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ionospheric:
	"""Ionospheric commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ionospheric", core, parent)

	def get_create(self) -> str:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:IONospheric:CREate \n
		Stores the current assistance data settings into the selected acquisition file. The file extension (*.rs_ion) is assigned
		automatically. Refer to 'MMEMory Subsystem' for general information on file handling in the default and in a specific
		directory. \n
			:return: filename: string Filename or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:IONospheric:CREate?')
		return trim_str_response(response)

	def set_create(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:IONospheric:CREate \n
		Stores the current assistance data settings into the selected acquisition file. The file extension (*.rs_ion) is assigned
		automatically. Refer to 'MMEMory Subsystem' for general information on file handling in the default and in a specific
		directory. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:IONospheric:CREate {param}')
