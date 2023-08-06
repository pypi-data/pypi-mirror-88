from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bbmm2:
	"""Bbmm2 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bbmm2", core, parent)

	# noinspection PyTypeChecker
	def get_channels(self) -> enums.SystConfHsChannels:
		"""SCONfiguration:DIQ:BBMM2:CHANnels \n
		No command help available \n
			:return: dig_iq_hs_bbmm_2_cha: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:DIQ:BBMM2:CHANnels?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfHsChannels)

	def set_channels(self, dig_iq_hs_bbmm_2_cha: enums.SystConfHsChannels) -> None:
		"""SCONfiguration:DIQ:BBMM2:CHANnels \n
		No command help available \n
			:param dig_iq_hs_bbmm_2_cha: No help available
		"""
		param = Conversions.enum_scalar_to_str(dig_iq_hs_bbmm_2_cha, enums.SystConfHsChannels)
		self._core.io.write(f'SCONfiguration:DIQ:BBMM2:CHANnels {param}')
