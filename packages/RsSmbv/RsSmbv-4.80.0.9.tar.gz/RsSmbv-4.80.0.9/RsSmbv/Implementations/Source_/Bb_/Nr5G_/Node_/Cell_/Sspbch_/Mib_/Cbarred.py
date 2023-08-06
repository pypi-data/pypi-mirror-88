from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cbarred:
	"""Cbarred commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cbarred", core, parent)

	def set(self, ssp_bch_cell_barre: enums.CellBarring, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:MIB:CBARred \n
		Cell barring is system information that indicates if UEs can camp on the particular cell NBAR or not BARR. \n
			:param ssp_bch_cell_barre: BARR| NBAR
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		param = Conversions.enum_scalar_to_str(ssp_bch_cell_barre, enums.CellBarring)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:MIB:CBARred {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.CellBarring:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:MIB:CBARred \n
		Cell barring is system information that indicates if UEs can camp on the particular cell NBAR or not BARR. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: ssp_bch_cell_barre: BARR| NBAR"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:MIB:CBARred?')
		return Conversions.str_to_scalar_enum(response, enums.CellBarring)
