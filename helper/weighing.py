import serial
import serial.tools.list_ports

class WeighingConnection(serial.Serial):

    def get_data(self):
        data = []
        data_dict = {}
        try:
            record = self.readlines()
            if record:
                print("hello weighing")
                data_dict['date']= record[0].decode('utf-8').split(' ')[-1].strip('\r\n')
                data_dict['time'] = record[1].decode('utf-8').split(' ')[-1].strip('\r\n')
                data_dict['gross']=  float(record[2].decode('utf-8').split(' ')[-1].strip('\r\n').split('kg')[0])

                return  data_dict
                    
        except KeyboardInterrupt:
            print("Closing the serial port.")
            self.close()


class WeighingScaleConnection():

    def __init__(self):
        self.connection = self.connect()


    def connect(self):
        connection = False
        if serial.tools.list_ports.comports():
            weighing_port = str(serial.tools.list_ports.comports()[0]).split(' ')[0]
            weighing_baudrate = 9600
            connection = WeighingConnection(port = weighing_port,baudrate = weighing_baudrate ,timeout =1 )
        else:
            print('no device connected')
        
        return connection


# con = WeighingScaleConnection().connection
# print(con)
# print(con.get_data())