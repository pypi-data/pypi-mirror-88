from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mops:
	"""Mops commands group definition. 11 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mops", core, parent)

	def clone(self) -> 'Mops':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mops(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def importPy(self):
		"""importPy commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_importPy'):
			from .Mops_.ImportPy import ImportPy
			self._importPy = ImportPy(self._core, self._base)
		return self._importPy

	# noinspection PyTypeChecker
	def get_display(self) -> enums.IonoGridView:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:DISPlay \n
		Toggles between indication of the vertical delay and GIVEI values. \n
			:return: display_type: GIVei| VDELay
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:DISPlay?')
		return Conversions.str_to_scalar_enum(response, enums.IonoGridView)

	def set_display(self, display_type: enums.IonoGridView) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:DISPlay \n
		Toggles between indication of the vertical delay and GIVEI values. \n
			:param display_type: GIVei| VDELay
		"""
		param = Conversions.enum_scalar_to_str(display_type, enums.IonoGridView)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:DISPlay {param}')

	def export(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:EXPort \n
		Saves the current ionospheric grid configuration in a file. \n
			:param filename: string Specify the file path, filename and extension. Allowed file extensions are *.rs_ion or *.iono_grid.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:EXPort {param}')

	def get_file(self) -> str:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:FILE \n
		Select a ionospheric grid file. \n
			:return: filename: string To load a predefined file, specify only the filename. To load a user-defined file, specify the absolute file path with filename and extension (*.iono_grid) .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:FILE?')
		return trim_str_response(response)

	def set_file(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:FILE \n
		Select a ionospheric grid file. \n
			:param filename: string To load a predefined file, specify only the filename. To load a user-defined file, specify the absolute file path with filename and extension (*.iono_grid) .
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:FILE {param}')
