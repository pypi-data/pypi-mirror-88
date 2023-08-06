from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Directory:
	"""Directory commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("directory", core, parent)

	def clear(self) -> None:
		"""HCOPy:FILE:[NAME]:AUTO:DIRectory:CLEar \n
		Deletes all files with extensions *.bmp, *.jpg, *.png and *.xpm in the directory set for automatic naming. \n
		"""
		self._core.io.write(f'HCOPy:FILE:NAME:AUTO:DIRectory:CLEar')

	def clear_with_opc(self) -> None:
		"""HCOPy:FILE:[NAME]:AUTO:DIRectory:CLEar \n
		Deletes all files with extensions *.bmp, *.jpg, *.png and *.xpm in the directory set for automatic naming. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'HCOPy:FILE:NAME:AUTO:DIRectory:CLEar')

	def get_value(self) -> str:
		"""HCOPy:FILE:[NAME]:AUTO:DIRectory \n
		Determines the path to save the hard copy, if you have enabled Automatic Naming. If the directory does not yet exist, the
		instrument automatically creates a new directory, using the instrument name and /var/user/ by default. \n
			:return: directory: string
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO:DIRectory?')
		return trim_str_response(response)

	def set_value(self, directory: str) -> None:
		"""HCOPy:FILE:[NAME]:AUTO:DIRectory \n
		Determines the path to save the hard copy, if you have enabled Automatic Naming. If the directory does not yet exist, the
		instrument automatically creates a new directory, using the instrument name and /var/user/ by default. \n
			:param directory: string
		"""
		param = Conversions.value_to_quoted_str(directory)
		self._core.io.write(f'HCOPy:FILE:NAME:AUTO:DIRectory {param}')
