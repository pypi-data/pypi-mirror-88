from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pinterval:
	"""Pinterval commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pinterval", core, parent)

	def set(self, pinterval: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:PINTerval \n
		The command sets the interval between two data packets for F-PDCH. The range depends on the ARB settings sequence length
		(method RsSmbv.Source.Bb.C2K.slength) . The values 80 ms, 40 ms, 20 ms, 10 ms and 5 ms can always be set, and the maximum
		value is 2000 ms. All intermediate values must satisfy the condition: Sequence Length * 80ms/2^n, where n is a whole
		number. \n
			:param pinterval: float Range: 5 ms to 2000 ms
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.decimal_value_to_str(pinterval)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:PINTerval {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:PINTerval \n
		The command sets the interval between two data packets for F-PDCH. The range depends on the ARB settings sequence length
		(method RsSmbv.Source.Bb.C2K.slength) . The values 80 ms, 40 ms, 20 ms, 10 ms and 5 ms can always be set, and the maximum
		value is 2000 ms. All intermediate values must satisfy the condition: Sequence Length * 80ms/2^n, where n is a whole
		number. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: pinterval: float Range: 5 ms to 2000 ms"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:PINTerval?')
		return Conversions.str_to_float(response)
