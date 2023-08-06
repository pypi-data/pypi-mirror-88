from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signature:
	"""Signature commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signature", core, parent)

	def set(self, signature: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:SIGNature \n
		The command selects the signature of the PCPCH (see Table 3 in 3GPP TS 25.213 Version 3.4.0 Release 1999) . \n
			:param signature: integer Range: 0 to 15
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(signature)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:SIGNature {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:SIGNature \n
		The command selects the signature of the PCPCH (see Table 3 in 3GPP TS 25.213 Version 3.4.0 Release 1999) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: signature: integer Range: 0 to 15"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:SIGNature?')
		return Conversions.str_to_int(response)
