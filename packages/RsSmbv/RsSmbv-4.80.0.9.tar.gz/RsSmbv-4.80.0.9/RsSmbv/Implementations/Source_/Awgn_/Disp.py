from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Disp:
	"""Disp commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("disp", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.NoisAwgnDispMode:
		"""[SOURce<HW>]:AWGN:DISP:MODE \n
		Sets the output to that the AWGN settings are related. \n
			:return: mode: RFA| IQOUT1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:DISP:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.NoisAwgnDispMode)

	# noinspection PyTypeChecker
	def get_oresults(self) -> enums.NoisAwgnDispOutpMode:
		"""[SOURce<HW>]:AWGN:DISP:ORESults \n
		No command help available \n
			:return: orrsults: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:DISP:ORESults?')
		return Conversions.str_to_scalar_enum(response, enums.NoisAwgnDispOutpMode)

	def set_oresults(self, orrsults: enums.NoisAwgnDispOutpMode) -> None:
		"""[SOURce<HW>]:AWGN:DISP:ORESults \n
		No command help available \n
			:param orrsults: No help available
		"""
		param = Conversions.enum_scalar_to_str(orrsults, enums.NoisAwgnDispOutpMode)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:DISP:ORESults {param}')
