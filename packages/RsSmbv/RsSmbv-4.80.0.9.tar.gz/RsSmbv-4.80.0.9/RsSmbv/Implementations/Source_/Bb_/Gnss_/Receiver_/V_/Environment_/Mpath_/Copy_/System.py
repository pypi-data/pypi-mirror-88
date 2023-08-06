from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class System:
	"""System commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("system", core, parent)

	def set(self, system_source: enums.Hybrid, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:MPATh:COPY:SYSTem \n
		Sets the GNSS system. If the copy to function is used, this setting refers to the target. \n
			:param system_source: GPS| GALileo| GLONass| BEIDou| QZSS| SBAS
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(system_source, enums.Hybrid)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:MPATh:COPY:SYSTem {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.Hybrid:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:MPATh:COPY:SYSTem \n
		Sets the GNSS system. If the copy to function is used, this setting refers to the target. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: system_source: GPS| GALileo| GLONass| BEIDou| QZSS| SBAS"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:MPATh:COPY:SYSTem?')
		return Conversions.str_to_scalar_enum(response, enums.Hybrid)
