from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bnc:
	"""Bnc commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bnc", core, parent)

	# noinspection PyTypeChecker
	def get_connection(self) -> enums.Test:
		"""TEST:BB:BNC:CONNection \n
		Queries the BNC connection test result. This is a password-protected function. Unlock the protection level 1 to access it.
		See SYSTem. \n
			:return: test_status: 0| 1| RUNning| STOPped
		"""
		response = self._core.io.query_str('TEST:BB:BNC:CONNection?')
		return Conversions.str_to_scalar_enum(response, enums.Test)

	# noinspection PyTypeChecker
	def get_destination(self) -> enums.TestBbBncConn:
		"""TEST:BB:BNC:DESTination \n
		Selects the BNC connection test destination. This is a password-protected function. Unlock the protection level 1 to
		access it. See SYSTem. \n
			:return: bnc_destination: AUTO| USER1| USER2| USER3| USER4| USER5
		"""
		response = self._core.io.query_str('TEST:BB:BNC:DESTination?')
		return Conversions.str_to_scalar_enum(response, enums.TestBbBncConn)

	def set_destination(self, bnc_destination: enums.TestBbBncConn) -> None:
		"""TEST:BB:BNC:DESTination \n
		Selects the BNC connection test destination. This is a password-protected function. Unlock the protection level 1 to
		access it. See SYSTem. \n
			:param bnc_destination: AUTO| USER1| USER2| USER3| USER4| USER5
		"""
		param = Conversions.enum_scalar_to_str(bnc_destination, enums.TestBbBncConn)
		self._core.io.write(f'TEST:BB:BNC:DESTination {param}')

	def get_log(self) -> str:
		"""TEST:BB:BNC:LOG \n
		Queries the log message reported during the BNC connector test. This is a password-protected function.
		Unlock the protection level 1 to access it. See SYSTem. \n
			:return: log: string
		"""
		response = self._core.io.query_str('TEST:BB:BNC:LOG?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TestBbBncConn:
		"""TEST:BB:BNC:SOURce \n
		Selects the BNC connection test source. This is a password-protected function. Unlock the protection level 1 to access it.
		See SYSTem. \n
			:return: bnc_source: AUTO| USER1| USER2| USER3| USER4| USER5| USER6| TRGA| TRGB| C1TMC1| C1TM2| C1TM3| C2TMC4| C2TM5| C2TM6| F1TMC1| F1TM2| F1TM3| F2TMC4| F2TM5| F2TM6| F3TMC1| F3TM2| F3TM3| F4TMC4| F4TM5| F4TM6
		"""
		response = self._core.io.query_str('TEST:BB:BNC:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TestBbBncConn)

	def set_source(self, bnc_source: enums.TestBbBncConn) -> None:
		"""TEST:BB:BNC:SOURce \n
		Selects the BNC connection test source. This is a password-protected function. Unlock the protection level 1 to access it.
		See SYSTem. \n
			:param bnc_source: AUTO| USER1| USER2| USER3| USER4| USER5| USER6| TRGA| TRGB| C1TMC1| C1TM2| C1TM3| C2TMC4| C2TM5| C2TM6| F1TMC1| F1TM2| F1TM3| F2TMC4| F2TM5| F2TM6| F3TMC1| F3TM2| F3TM3| F4TMC4| F4TM5| F4TM6
		"""
		param = Conversions.enum_scalar_to_str(bnc_source, enums.TestBbBncConn)
		self._core.io.write(f'TEST:BB:BNC:SOURce {param}')
