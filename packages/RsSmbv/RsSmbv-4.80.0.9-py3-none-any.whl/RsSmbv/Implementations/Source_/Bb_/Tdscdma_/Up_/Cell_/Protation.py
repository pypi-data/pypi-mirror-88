from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Protation:
	"""Protation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("protation", core, parent)

	def set(self, protation: enums.TdscdmaPhasRot, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:PROTation \n
		Selects the phase rotation for the downlink pilots. \n
			:param protation: AUTO| S1| S2 AUTO Default phase rotation sequence according to the presence of the P-CCPCH. S1 There is a P-CCPCH in the next four subframes. S2 There is no P-CCPCH in the next four subframes.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(protation, enums.TdscdmaPhasRot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:PROTation {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TdscdmaPhasRot:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:PROTation \n
		Selects the phase rotation for the downlink pilots. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: protation: AUTO| S1| S2 AUTO Default phase rotation sequence according to the presence of the P-CCPCH. S1 There is a P-CCPCH in the next four subframes. S2 There is no P-CCPCH in the next four subframes."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:PROTation?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaPhasRot)
