from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename

    def read(self) -> AggregatedData:
        """Retrieve data from sensors || Метод повертає дані отримані з датчиків"""
        if not (self.accelerometer_file and self.gps_file):
            raise ValueError("Files can't be retrieving for reading.")

        accelerometer_data = self._read_line_and_split(self.accelerometer_file)
        gps_data = self._read_line_and_split(self.gps_file)

        if accelerometer_data and gps_data:
            accelerometer = Accelerometer(*map(int, accelerometer_data))
            gps = Gps(*map(float, gps_data))
            time = datetime.now()
            return AggregatedData(accelerometer, gps, time, config.USER_ID)

    def startReading(self, *args, **kwargs):
        """Invoke before starting data reading || Метод повинен викликатись перед початком читання даних"""
        if not (self.accelerometer_file and self.gps_file):
            try:
                self.accelerometer_file = open(self.accelerometer_filename, 'r')
                self.gps_file = open(self.gps_filename, 'r')

                self._skip_header(self.accelerometer_file)
                self._skip_header(self.gps_file)
            except Exception as exception:
                print(f"Error retrieving files: {exception}")
                raise

    def stopReading(self, *args, **kwargs):
        """Invoke to finish data reading || Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_file or self.gps_file:
            self.accelerometer_file.close()
            self.gps_file.close()

    @staticmethod
    def _read_line_and_split(file):
        return file.readline().strip().split(',')

    @staticmethod
    def _skip_header(file):
        file.readline()
