from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plength:
	"""Plength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plength", core, parent)

	def set(self, plength: enums.PowPreContLen, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:PLENgth \n
		The command defines the length of the power control preamble of the PCPCH as a number of slots. \n
			:param plength: S0| S8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(plength, enums.PowPreContLen)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:PLENgth {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.PowPreContLen:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:PLENgth \n
		The command defines the length of the power control preamble of the PCPCH as a number of slots. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: plength: S0| S8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:PLENgth?')
		return Conversions.str_to_scalar_enum(response, enums.PowPreContLen)
