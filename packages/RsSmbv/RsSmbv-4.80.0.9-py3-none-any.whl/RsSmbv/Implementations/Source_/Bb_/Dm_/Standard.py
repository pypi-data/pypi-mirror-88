from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Standard:
	"""Standard commands group definition. 5 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standard", core, parent)

	def clone(self) -> 'Standard':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Standard(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ulist(self):
		"""ulist commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_ulist'):
			from .Standard_.Ulist import Ulist
			self._ulist = Ulist(self._core, self._base)
		return self._ulist

	# noinspection PyTypeChecker
	def get_value(self) -> enums.DmStan:
		"""[SOURce<HW>]:BB:DM:STANdard \n
		Selects predefined set of settings according to the selected standard, see Table 'Communication standards with their
		predefined settings'. \n
			:return: standard: USER| BLUetooth| DECT| ETC| GSM| GSMEdge| NADC| PDC| PHS| TETRa| W3GPp| TDSCdma| CFORward| CREVerse| WORLdspace| TFTS| APCOPH1C4fm| APCOPH1CQpsk| APCOPH2HCpm| APCOPH2HDQpsk| APCOPH2HD8PSKW| APCOPH2HD8PSKN| APCOPH1Lsm| APCOPH1Wcqpsk A query returns the value USER if one the following is true: • A user-defined custom digital modulation setting was loaded • One of the associated settings was changed subsequent to the selection of a standard.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.DmStan)

	def set_value(self, standard: enums.DmStan) -> None:
		"""[SOURce<HW>]:BB:DM:STANdard \n
		Selects predefined set of settings according to the selected standard, see Table 'Communication standards with their
		predefined settings'. \n
			:param standard: USER| BLUetooth| DECT| ETC| GSM| GSMEdge| NADC| PDC| PHS| TETRa| W3GPp| TDSCdma| CFORward| CREVerse| WORLdspace| TFTS| APCOPH1C4fm| APCOPH1CQpsk| APCOPH2HCpm| APCOPH2HDQpsk| APCOPH2HD8PSKW| APCOPH2HD8PSKN| APCOPH1Lsm| APCOPH1Wcqpsk A query returns the value USER if one the following is true: • A user-defined custom digital modulation setting was loaded • One of the associated settings was changed subsequent to the selection of a standard.
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.DmStan)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:STANdard {param}')
