from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lreference:
	"""Lreference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lreference", core, parent)

	def set(self, level_reference: enums.DpdPowRef, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:LREFerence \n
		Sets whether a dynamic (BDPD|ADPD) or a static (SDPS) adaptation of the range the selected DPD is applied on. \n
			:param level_reference: BDPD| ADPD| SDPD
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.enum_scalar_to_str(level_reference, enums.DpdPowRef)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:LREFerence {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.DpdPowRef:
		"""[SOURce<HW>]:IQ:DPD<ST>:LREFerence \n
		Sets whether a dynamic (BDPD|ADPD) or a static (SDPS) adaptation of the range the selected DPD is applied on. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: level_reference: BDPD| ADPD| SDPD"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:LREFerence?')
		return Conversions.str_to_scalar_enum(response, enums.DpdPowRef)
