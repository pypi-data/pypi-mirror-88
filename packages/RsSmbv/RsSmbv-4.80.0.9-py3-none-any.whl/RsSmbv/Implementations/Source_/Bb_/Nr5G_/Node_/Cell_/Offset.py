from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def set(self, offset_relative_t: enums.OffsetRelativeAll, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:OFFSet \n
		Defines the reference point, relative to which the SS/PBCH is allocated in frequency domain. \n
			:param offset_relative_t: TXBW| POINta TXBW The frequency position of the SS/PBCH is set relative to the usable RBs that apply for the current numerology, i.e. to the start of the TxBWs. POINta The frequency position of the SS/PBCH is set relative to the position of point A.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(offset_relative_t, enums.OffsetRelativeAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:OFFSet {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.OffsetRelativeAll:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:OFFSet \n
		Defines the reference point, relative to which the SS/PBCH is allocated in frequency domain. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: offset_relative_t: TXBW| POINta TXBW The frequency position of the SS/PBCH is set relative to the usable RBs that apply for the current numerology, i.e. to the start of the TxBWs. POINta The frequency position of the SS/PBCH is set relative to the position of point A."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:OFFSet?')
		return Conversions.str_to_scalar_enum(response, enums.OffsetRelativeAll)
