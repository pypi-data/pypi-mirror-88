from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Baseband:
	"""Baseband commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("baseband", core, parent)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SystConfBbConf:
		"""SCONfiguration:BASeband:SOURce \n
		No command help available \n
			:return: sour_config: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:BASeband:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfBbConf)

	def set_source(self, sour_config: enums.SystConfBbConf) -> None:
		"""SCONfiguration:BASeband:SOURce \n
		No command help available \n
			:param sour_config: No help available
		"""
		param = Conversions.enum_scalar_to_str(sour_config, enums.SystConfBbConf)
		self._core.io.write(f'SCONfiguration:BASeband:SOURce {param}')
