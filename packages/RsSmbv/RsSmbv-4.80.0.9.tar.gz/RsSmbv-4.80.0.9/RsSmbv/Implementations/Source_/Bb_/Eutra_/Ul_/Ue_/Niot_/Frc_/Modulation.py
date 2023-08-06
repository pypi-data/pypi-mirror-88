from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraUlueNbiotModulation:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:FRC:MODulation \n
		Queries the modulation scheme. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: modulation: QPSK| PI2Bpsk| PI4Qpsk"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:FRC:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUlueNbiotModulation)
