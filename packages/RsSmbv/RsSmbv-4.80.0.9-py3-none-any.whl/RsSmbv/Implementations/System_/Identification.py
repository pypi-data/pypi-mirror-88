from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Identification:
	"""Identification commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("identification", core, parent)

	def preset(self) -> None:
		"""SYSTem:IDENtification:PRESet \n
		Sets the *IDN and *OPT strings in user defined mode to default values. \n
		"""
		self._core.io.write(f'SYSTem:IDENtification:PRESet')

	def preset_with_opc(self) -> None:
		"""SYSTem:IDENtification:PRESet \n
		Sets the *IDN and *OPT strings in user defined mode to default values. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:IDENtification:PRESet')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.AutoUser:
		"""SYSTem:IDENtification \n
		Selects the mode to determine the 'IDN String' and the 'OPT String' for the instrument, selected with command method
		RsSmbv.System.language. Note: While working in an emulation mode, the R&S SMBV100B specific command set is disabled, that
		is, the SCPI command method RsSmbv.System.Identification.value is discarded. \n
			:return: identification: AUTO| USER AUTO Automatically determines the strings. USER User-defined strings can be selected.
		"""
		response = self._core.io.query_str('SYSTem:IDENtification?')
		return Conversions.str_to_scalar_enum(response, enums.AutoUser)

	def set_value(self, identification: enums.AutoUser) -> None:
		"""SYSTem:IDENtification \n
		Selects the mode to determine the 'IDN String' and the 'OPT String' for the instrument, selected with command method
		RsSmbv.System.language. Note: While working in an emulation mode, the R&S SMBV100B specific command set is disabled, that
		is, the SCPI command method RsSmbv.System.Identification.value is discarded. \n
			:param identification: AUTO| USER AUTO Automatically determines the strings. USER User-defined strings can be selected.
		"""
		param = Conversions.enum_scalar_to_str(identification, enums.AutoUser)
		self._core.io.write(f'SYSTem:IDENtification {param}')
