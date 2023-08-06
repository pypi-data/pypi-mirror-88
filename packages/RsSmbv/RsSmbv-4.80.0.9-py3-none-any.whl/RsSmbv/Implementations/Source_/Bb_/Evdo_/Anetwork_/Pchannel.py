from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pchannel:
	"""Pchannel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pchannel", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:PCHannel:STATe \n
		Displays the state of the pilot channel. Pilot channel is transmitted by sector on each active forward channel.
		It is present always and transmitted at the full sector power. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:PCHannel:STATe?')
		return Conversions.str_to_bool(response)
