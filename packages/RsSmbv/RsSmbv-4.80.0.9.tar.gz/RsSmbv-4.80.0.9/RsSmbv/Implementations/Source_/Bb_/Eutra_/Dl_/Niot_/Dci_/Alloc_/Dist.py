from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dist:
	"""Dist commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dist", core, parent)

	def set(self, dist_npdcch_npdsc: enums.EutraNbIoTdCiDistNpdcchNpdsch, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:DIST \n
		Sets how the distance between the NPDCCH to NPDSCH is determined. \n
			:param dist_npdcch_npdsc: STD| MIN| ZERO ZERO disables the NPDSCH SIB1-NR and NPUCCH transmissions. The NPDSCH is transmitted immediately after the NPDCCH. Use this value to increase the number of NPDSCH allocations.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(dist_npdcch_npdsc, enums.EutraNbIoTdCiDistNpdcchNpdsch)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:DIST {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraNbIoTdCiDistNpdcchNpdsch:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:DIST \n
		Sets how the distance between the NPDCCH to NPDSCH is determined. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: dist_npdcch_npdsc: STD| MIN| ZERO ZERO disables the NPDSCH SIB1-NR and NPUCCH transmissions. The NPDSCH is transmitted immediately after the NPDCCH. Use this value to increase the number of NPDSCH allocations."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:DIST?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbIoTdCiDistNpdcchNpdsch)
