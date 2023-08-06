from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cbw:
	"""Cbw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cbw", core, parent)

	def set(self, chan_band_width: enums.Nr5Gcbw, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:CBW \n
		Selects the bandwidth of the node carrier. \n
			:param chan_band_width: BW5| BW10| BW15| BW20| BW25| BW40| BW50| BW60| BW100| BW80| BW400| BW200| BW30| BW70| BW90
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(chan_band_width, enums.Nr5Gcbw)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:CBW {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.Nr5Gcbw:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:CBW \n
		Selects the bandwidth of the node carrier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: chan_band_width: BW5| BW10| BW15| BW20| BW25| BW40| BW50| BW60| BW100| BW80| BW400| BW200| BW30| BW70| BW90"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:CBW?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5Gcbw)
