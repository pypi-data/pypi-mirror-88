from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Schannel:
	"""Schannel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("schannel", core, parent)

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:SCHannel:COUNt \n
		Sets the number of supplemental channels. The maximum number of supplemental channels depends on the selected radio
		configuration. The setting takes effect only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.
		set. It is specific for the selected radio configuration. \n
			:return: count: integer Range: 0 to 7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:SCHannel:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:SCHannel:COUNt \n
		Sets the number of supplemental channels. The maximum number of supplemental channels depends on the selected radio
		configuration. The setting takes effect only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.
		set. It is specific for the selected radio configuration. \n
			:param count: integer Range: 0 to 7
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:SCHannel:COUNt {param}')
