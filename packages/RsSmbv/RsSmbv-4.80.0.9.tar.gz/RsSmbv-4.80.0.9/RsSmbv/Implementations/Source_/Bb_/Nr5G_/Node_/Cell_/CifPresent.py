from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CifPresent:
	"""CifPresent commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cifPresent", core, parent)

	def set(self, cif_present: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:CIFPresent \n
		Defines whether the carrier indicator field (CIF) is included in the PDCCH DCI formats transmitted from the corresponding
		cell. The CIF is present in each DCI format and identifies the component carrier that carries the PDSCH or PUSCH for the
		particular PDCCH in the cross-carrier approach. According to the 5G NR specification, cross-carrier scheduling is enabled
		by higher-level signaling. To simulate a cross-carrier scheduling in this implementation, enable the 'Node > Carriers >
		CIF Present' per each cell. \n
			:param cif_present: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.bool_to_str(cif_present)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:CIFPresent {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:CIFPresent \n
		Defines whether the carrier indicator field (CIF) is included in the PDCCH DCI formats transmitted from the corresponding
		cell. The CIF is present in each DCI format and identifies the component carrier that carries the PDSCH or PUSCH for the
		particular PDCCH in the cross-carrier approach. According to the 5G NR specification, cross-carrier scheduling is enabled
		by higher-level signaling. To simulate a cross-carrier scheduling in this implementation, enable the 'Node > Carriers >
		CIF Present' per each cell. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: cif_present: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:CIFPresent?')
		return Conversions.str_to_bool(response)
