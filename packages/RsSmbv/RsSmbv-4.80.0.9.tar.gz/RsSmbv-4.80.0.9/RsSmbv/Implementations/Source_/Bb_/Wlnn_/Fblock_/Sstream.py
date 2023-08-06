from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sstream:
	"""Sstream commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sstream", core, parent)

	def set(self, sstream: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SSTReam \n
		Sets the number of the spatial streams. For physical mode LEGACY, only value 1 is valid. For Tx Mode 'HT-Duplicate', only
		value 1 is valid. In all other cases, the number of spatial streams depends on the number of antennas configured with
		command method RsSmbv.Source.Bb.Wlnn.Antenna.mode. \n
			:param sstream: integer Range: 1 to 8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.decimal_value_to_str(sstream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SSTReam {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SSTReam \n
		Sets the number of the spatial streams. For physical mode LEGACY, only value 1 is valid. For Tx Mode 'HT-Duplicate', only
		value 1 is valid. In all other cases, the number of spatial streams depends on the number of antennas configured with
		command method RsSmbv.Source.Bb.Wlnn.Antenna.mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: sstream: integer Range: 1 to 8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SSTReam?')
		return Conversions.str_to_int(response)
