from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LmVariation:
	"""LmVariation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lmVariation", core, parent)

	def set(self, lmv: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:LMVariation \n
		Sets the local magnetic variation. \n
			:param lmv: float A positive value represents an east variation (clockwise from true north) Range: -180 to 180, Unit: deg
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(lmv)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:LMVariation {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:LMVariation \n
		Sets the local magnetic variation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: lmv: float A positive value represents an east variation (clockwise from true north) Range: -180 to 180, Unit: deg"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:LMVariation?')
		return Conversions.str_to_float(response)
