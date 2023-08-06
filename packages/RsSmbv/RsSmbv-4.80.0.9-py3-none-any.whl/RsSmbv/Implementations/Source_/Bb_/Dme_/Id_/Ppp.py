from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ppp:
	"""Ppp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ppp", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:ID:PPP:[STATe] \n
		Sets the state of the pair of pulse pairs for the ID signal generation. When enabled a pair of pulse pairs is transmitted
		during the set method RsSmbv.Source.Bb.Dme.Id.rate. \n
			:return: pair_of_pulse_pair: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:PPP:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, pair_of_pulse_pair: bool) -> None:
		"""[SOURce<HW>]:[BB]:DME:ID:PPP:[STATe] \n
		Sets the state of the pair of pulse pairs for the ID signal generation. When enabled a pair of pulse pairs is transmitted
		during the set method RsSmbv.Source.Bb.Dme.Id.rate. \n
			:param pair_of_pulse_pair: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(pair_of_pulse_pair)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:PPP:STATe {param}')
