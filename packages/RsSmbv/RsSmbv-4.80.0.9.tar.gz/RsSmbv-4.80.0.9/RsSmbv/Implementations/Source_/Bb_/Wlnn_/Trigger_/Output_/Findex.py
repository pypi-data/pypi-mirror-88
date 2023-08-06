from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Findex:
	"""Findex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("findex", core, parent)

	def set(self, fi_ndex: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:FINDex \n
		Sets the frame index, that is, the frame to be marked in the frame block marked with method RsSmbv.Source.Bb.Wlnn.Trigger.
		Output.FbIndex.set. The maximum value depends on the number of frames set with command method RsSmbv.Source.Bb.Wlnn.
		Fblock.Fcount.set . The maximum value is 1024. \n
			:param fi_ndex: integer Range: 1 to 1024
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(fi_ndex)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:FINDex {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:FINDex \n
		Sets the frame index, that is, the frame to be marked in the frame block marked with method RsSmbv.Source.Bb.Wlnn.Trigger.
		Output.FbIndex.set. The maximum value depends on the number of frames set with command method RsSmbv.Source.Bb.Wlnn.
		Fblock.Fcount.set . The maximum value is 1024. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: fi_ndex: integer Range: 1 to 1024"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:FINDex?')
		return Conversions.str_to_int(response)
