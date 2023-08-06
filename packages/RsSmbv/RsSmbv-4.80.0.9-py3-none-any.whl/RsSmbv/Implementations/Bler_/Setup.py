from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setup:
	"""Setup commands group definition. 7 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setup", core, parent)

	def clone(self) -> 'Setup':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Setup(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Setup_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	# noinspection PyTypeChecker
	def get_corder(self) -> enums.BertCrcOrder:
		"""BLER:SETup:CORDer \n
		Sets the byte order of the checksum (CRC) . \n
			:return: corder: LSB| MSB LSB The checksum starts with the least significant byte. MSB The checksum starts with the most significant byte.
		"""
		response = self._core.io.query_str('BLER:SETup:CORDer?')
		return Conversions.str_to_scalar_enum(response, enums.BertCrcOrder)

	def set_corder(self, corder: enums.BertCrcOrder) -> None:
		"""BLER:SETup:CORDer \n
		Sets the byte order of the checksum (CRC) . \n
			:param corder: LSB| MSB LSB The checksum starts with the least significant byte. MSB The checksum starts with the most significant byte.
		"""
		param = Conversions.enum_scalar_to_str(corder, enums.BertCrcOrder)
		self._core.io.write(f'BLER:SETup:CORDer {param}')

	# noinspection PyTypeChecker
	def get_denable(self) -> enums.LowHigh:
		"""BLER:SETup:DENable \n
		Activates the Data Enable signal and, if activated, sets its polarity. The signal marks the data that is evaluated by the
		BERT/BLER measurement. Does not evaluate data supplied by the DUT, that is additional to the PRBS sequence (e.g. sync,
		preambles, other channels, etc.) . \n
			:return: denable: HIGH| LOW OFF Ignore any signal at the data enable input; use all data at the BERT/BLER data input for the measurement. HIGH Use the data enable signal. Only measures the data at the BERT/BLER data input during a high level of the data enable signal. Interrupts the measurement during a low level. LOW Use the data enable signal. Only measures the data at the BERT/BLER data input during a low level of the data enable signal. Interrupts the measurement during a high level.
		"""
		response = self._core.io.query_str('BLER:SETup:DENable?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_denable(self, denable: enums.LowHigh) -> None:
		"""BLER:SETup:DENable \n
		Activates the Data Enable signal and, if activated, sets its polarity. The signal marks the data that is evaluated by the
		BERT/BLER measurement. Does not evaluate data supplied by the DUT, that is additional to the PRBS sequence (e.g. sync,
		preambles, other channels, etc.) . \n
			:param denable: HIGH| LOW OFF Ignore any signal at the data enable input; use all data at the BERT/BLER data input for the measurement. HIGH Use the data enable signal. Only measures the data at the BERT/BLER data input during a high level of the data enable signal. Interrupts the measurement during a low level. LOW Use the data enable signal. Only measures the data at the BERT/BLER data input during a low level of the data enable signal. Interrupts the measurement during a high level.
		"""
		param = Conversions.enum_scalar_to_str(denable, enums.LowHigh)
		self._core.io.write(f'BLER:SETup:DENable {param}')

	def get_mcount(self) -> int:
		"""BLER:SETup:MCOunt \n
		Enters the number of transmitted data bits/data blocks to be checked before the measurement is terminated. A BERT/BLER
		measurement does not count data suppressed by method RsSmbv.Bert.Setup.denable|method RsSmbv.Bler.Setup.denable.
		This termination criteria always terminates the measurement after the specified number of data bits/data blocks. Starting
		from this point, outputs the fourth value with 1 (= terminate measurement) if the result is queried. For the continuous
		measurement mode, the measurement restarts once the results have been queried. \n
			:return: mcount: integer Range: 0 to 4294967295
		"""
		response = self._core.io.query_str('BLER:SETup:MCOunt?')
		return Conversions.str_to_int(response)

	def set_mcount(self, mcount: int) -> None:
		"""BLER:SETup:MCOunt \n
		Enters the number of transmitted data bits/data blocks to be checked before the measurement is terminated. A BERT/BLER
		measurement does not count data suppressed by method RsSmbv.Bert.Setup.denable|method RsSmbv.Bler.Setup.denable.
		This termination criteria always terminates the measurement after the specified number of data bits/data blocks. Starting
		from this point, outputs the fourth value with 1 (= terminate measurement) if the result is queried. For the continuous
		measurement mode, the measurement restarts once the results have been queried. \n
			:param mcount: integer Range: 0 to 4294967295
		"""
		param = Conversions.decimal_value_to_str(mcount)
		self._core.io.write(f'BLER:SETup:MCOunt {param}')

	def get_merror(self) -> int:
		"""BLER:SETup:MERRor \n
		Enters the number of errors to occur before the measurement is terminated. This termination criterion always terminates
		the measurement after the specified number of errors. Starting from this point, outputs the fourth value with 1 (=
		terminate measurement) if the measurement result is queried. \n
			:return: me_rror: integer Range: 0 to 4294967295
		"""
		response = self._core.io.query_str('BLER:SETup:MERRor?')
		return Conversions.str_to_int(response)

	def set_merror(self, me_rror: int) -> None:
		"""BLER:SETup:MERRor \n
		Enters the number of errors to occur before the measurement is terminated. This termination criterion always terminates
		the measurement after the specified number of errors. Starting from this point, outputs the fourth value with 1 (=
		terminate measurement) if the measurement result is queried. \n
			:param me_rror: integer Range: 0 to 4294967295
		"""
		param = Conversions.decimal_value_to_str(me_rror)
		self._core.io.write(f'BLER:SETup:MERRor {param}')

	def get_timeout(self) -> float:
		"""BLER:SETup:TIMeout \n
		Sets the timeout. \n
			:return: timeout: float Range: 0.1 to 1
		"""
		response = self._core.io.query_str('BLER:SETup:TIMeout?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""BLER:SETup:TIMeout \n
		Sets the timeout. \n
			:param timeout: float Range: 0.1 to 1
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'BLER:SETup:TIMeout {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.BertType:
		"""BLER:SETup:TYPE \n
		Queries the used CRC polynomial. \n
			:return: type_py: CRC16 CCITT CRC 16 : G(x) = x16 + x12 + x5 + x1
		"""
		response = self._core.io.query_str('BLER:SETup:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.BertType)

	def set_type_py(self, type_py: enums.BertType) -> None:
		"""BLER:SETup:TYPE \n
		Queries the used CRC polynomial. \n
			:param type_py: CRC16 CCITT CRC 16 : G(x) = x16 + x12 + x5 + x1
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.BertType)
		self._core.io.write(f'BLER:SETup:TYPE {param}')
