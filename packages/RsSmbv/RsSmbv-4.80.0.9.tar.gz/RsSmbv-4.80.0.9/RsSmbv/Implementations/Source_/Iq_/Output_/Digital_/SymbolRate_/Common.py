from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Common:
	"""Common commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("common", core, parent)

	def get_state(self) -> bool:
		"""[SOURce]:IQ:OUTPut:DIGital:SRATe:COMMon:STATe \n
		If enabled, the same sample rate value is applied to all channels. \n
			:return: dig_iq_hs_com_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce:IQ:OUTPut:DIGital:SRATe:COMMon:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, dig_iq_hs_com_state: bool) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:SRATe:COMMon:STATe \n
		If enabled, the same sample rate value is applied to all channels. \n
			:param dig_iq_hs_com_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(dig_iq_hs_com_state)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:SRATe:COMMon:STATe {param}')
