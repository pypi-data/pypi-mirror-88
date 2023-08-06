from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sync:
	"""Sync commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sync", core, parent)

	def get_cnumber(self) -> int:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:CNUMber \n
		Sets the CDMA Channel Number which corresponds to the RF. \n
			:return: cnumber: integer Range: 0 to 2047
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:BSTation:SYNC:CNUMber?')
		return Conversions.str_to_int(response)

	def set_cnumber(self, cnumber: int) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:CNUMber \n
		Sets the CDMA Channel Number which corresponds to the RF. \n
			:param cnumber: integer Range: 0 to 2047
		"""
		param = Conversions.decimal_value_to_str(cnumber)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation:SYNC:CNUMber {param}')

	# noinspection PyTypeChecker
	def get_mprev(self) -> enums.MinPrEv:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:MPRev \n
		Sets the Minimum Protocol Revision Level. The base station sets this field to prevent mobile stations which cannot be
		supported by the base station from accessing the CDMA system. \n
			:return: mprev: 2| 8 Range: 2 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:BSTation:SYNC:MPRev?')
		return Conversions.str_to_scalar_enum(response, enums.MinPrEv)

	def set_mprev(self, mprev: enums.MinPrEv) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:MPRev \n
		Sets the Minimum Protocol Revision Level. The base station sets this field to prevent mobile stations which cannot be
		supported by the base station from accessing the CDMA system. \n
			:param mprev: 2| 8 Range: 2 to 8
		"""
		param = Conversions.enum_scalar_to_str(mprev, enums.MinPrEv)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation:SYNC:MPRev {param}')

	def get_nid(self) -> int:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:NID \n
		Sets the Network Identification. The NID serves as a sub-identifier of a CDMA system as defined by the owner of the SID. \n
			:return: nid: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:BSTation:SYNC:NID?')
		return Conversions.str_to_int(response)

	def set_nid(self, nid: int) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:NID \n
		Sets the Network Identification. The NID serves as a sub-identifier of a CDMA system as defined by the owner of the SID. \n
			:param nid: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(nid)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation:SYNC:NID {param}')

	def get_prev(self) -> int:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:PREV \n
		Sets the Protocol Revision Level, i.e. specifies the CDMA2000 system release number. The table below gives the
		cross-reference between the P_REV values and the CDMA2000 Releases.
			Table Header: P_REV / CDMA2000 Release \n
			- 1 / Korean PCS(Band Class4) , USPCS(Band Class1)
			- 2 / IS-95
			- 3 / TBS74
			- 4 / IS-95A
			- 5 / IS-95B
			- 6 / IS2000 Release 0
			- 7 / IS2000 Release A
			- 8 / IS2000 Release B \n
			:return: prev: integer Range: 1 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:BSTation:SYNC:PREV?')
		return Conversions.str_to_int(response)

	def set_prev(self, prev: int) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:PREV \n
		Sets the Protocol Revision Level, i.e. specifies the CDMA2000 system release number. The table below gives the
		cross-reference between the P_REV values and the CDMA2000 Releases.
			Table Header: P_REV / CDMA2000 Release \n
			- 1 / Korean PCS(Band Class4) , USPCS(Band Class1)
			- 2 / IS-95
			- 3 / TBS74
			- 4 / IS-95A
			- 5 / IS-95B
			- 6 / IS2000 Release 0
			- 7 / IS2000 Release A
			- 8 / IS2000 Release B \n
			:param prev: integer Range: 1 to 8
		"""
		param = Conversions.decimal_value_to_str(prev)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation:SYNC:PREV {param}')

	def get_sid(self) -> int:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:SID \n
		Displays the System Identification. The base station sets the system identification number. \n
			:return: sid: integer Range: 0 to 32767
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:BSTation:SYNC:SID?')
		return Conversions.str_to_int(response)

	def set_sid(self, sid: int) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:SYNC:SID \n
		Displays the System Identification. The base station sets the system identification number. \n
			:param sid: integer Range: 0 to 32767
		"""
		param = Conversions.decimal_value_to_str(sid)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation:SYNC:SID {param}')
