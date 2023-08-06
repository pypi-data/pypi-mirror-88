from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Method:
	"""Method commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("method", core, parent)

	def set(self, method: enums.CmMethUp, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:CMODe:METHod \n
		The command selects compressed mode method. \n
			:param method: HLSCheduling| SF2 SF2 The data is compressed by halving the spreading factor. HLSCheduling The data is compressed by stopping the transmission of the data stream during the transmission gap.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(method, enums.CmMethUp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:CMODe:METHod {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.CmMethUp:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:CMODe:METHod \n
		The command selects compressed mode method. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: method: HLSCheduling| SF2 SF2 The data is compressed by halving the spreading factor. HLSCheduling The data is compressed by stopping the transmission of the data stream during the transmission gap."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:CMODe:METHod?')
		return Conversions.str_to_scalar_enum(response, enums.CmMethUp)
