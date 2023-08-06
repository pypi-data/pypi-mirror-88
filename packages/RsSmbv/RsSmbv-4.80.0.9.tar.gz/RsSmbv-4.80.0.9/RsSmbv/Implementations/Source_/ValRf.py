from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValRf:
	"""ValRf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("valRf", core, parent)

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SlopeType:
		"""[SOURce<HW>]:VALRf:SLOPe \n
		No command help available \n
			:return: sig_valid_slope: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VALRf:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)

	def set_slope(self, sig_valid_slope: enums.SlopeType) -> None:
		"""[SOURce<HW>]:VALRf:SLOPe \n
		No command help available \n
			:param sig_valid_slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(sig_valid_slope, enums.SlopeType)
		self._core.io.write(f'SOURce<HwInstance>:VALRf:SLOPe {param}')
