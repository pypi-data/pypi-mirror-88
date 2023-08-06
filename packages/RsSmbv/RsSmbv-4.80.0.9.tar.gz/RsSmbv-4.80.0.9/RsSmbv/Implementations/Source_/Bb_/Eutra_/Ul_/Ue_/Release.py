from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Release:
	"""Release commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("release", core, parent)

	def set(self, release: enums.EutraUeRelease, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:RELease \n
		Sets which LTE release version the UE supports. \n
			:param release: R89| LADV | EMTC| NIOT
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(release, enums.EutraUeRelease)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:RELease {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraUeRelease:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:RELease \n
		Sets which LTE release version the UE supports. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: release: R89| LADV | EMTC| NIOT"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:RELease?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUeRelease)
