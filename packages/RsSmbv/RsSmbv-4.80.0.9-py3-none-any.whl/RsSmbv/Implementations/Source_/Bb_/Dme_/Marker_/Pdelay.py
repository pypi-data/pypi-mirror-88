from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pdelay:
	"""Pdelay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pdelay", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:PDELay \n
		Queries the marker processing delay, internally measured value. This command is available only for method RsSmbv.Source.
		Bb.Dme.Marker.Mode.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:return: processed_delay: float Range: 0 to 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:PDELay?')
		return Conversions.str_to_float(response)
