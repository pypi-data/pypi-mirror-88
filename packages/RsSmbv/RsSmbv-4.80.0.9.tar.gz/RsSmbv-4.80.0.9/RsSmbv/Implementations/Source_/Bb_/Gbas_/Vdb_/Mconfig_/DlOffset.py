from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DlOffset:
	"""DlOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dlOffset", core, parent)

	def set(self, del_len_off: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DLOFfset \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the delta length offset. \n
			:param del_len_off: float Range: 0 to 2032
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(del_len_off)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:DLOFfset {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DLOFfset \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the delta length offset. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: del_len_off: float Range: 0 to 2032"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:DLOFfset?')
		return Conversions.str_to_float(response)
