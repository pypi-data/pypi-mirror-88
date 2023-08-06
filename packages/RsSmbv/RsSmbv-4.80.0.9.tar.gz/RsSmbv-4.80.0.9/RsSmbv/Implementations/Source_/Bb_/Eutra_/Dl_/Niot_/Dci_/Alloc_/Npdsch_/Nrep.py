from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nrep:
	"""Nrep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nrep", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:NPDSch:NREP \n
		Queries the number of repetitions of NPDSCH (NRep.) \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: np_dsch_rpt: integer Range: 1 to 2048"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:NPDSch:NREP?')
		return Conversions.str_to_int(response)
