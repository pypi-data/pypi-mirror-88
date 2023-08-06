from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TbSize:
	"""TbSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbSize", core, parent)

	def set(self, tb_size: int, transportChannel=repcap.TransportChannel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:TBSize \n
		Sets the size of the data blocks. \n
			:param tb_size: integer
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.decimal_value_to_str(tb_size)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:TBSize {param}')

	def get(self, transportChannel=repcap.TransportChannel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:TBSize \n
		Sets the size of the data blocks. \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: tb_size: integer"""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:TBSize?')
		return Conversions.str_to_int(response)
