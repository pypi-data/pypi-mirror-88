import smbus2
import time

bus = smbus2.SMBus(1)

class DCMotor:
    def __init__(self,pca9685_addr = 0x60,motorSet = [4,3,2,1]):
        # 設定PRESCALE PWM frequency = 50Hz
        bus.write_i2c_block_data(pca9685_addr, 0xFE, [121])   
        # 離開睡眠模式
        bus.write_i2c_block_data(pca9685_addr, 0x00, [0x01])
        self.motorSet = motorSet

#    def set_PWM_ON(self, addr , ch, value):
#        low_byte_val  =   value & 0x00FF 
#        high_byte_val = ( value & 0x0F00 ) >> 8
#        reg_low_byte = 0x06 + 4 * ch 
#        bus.write_i2c_block_data(addr, reg_low_byte    , [low_byte_val ])
#        bus.write_i2c_block_data(addr, reg_low_byte + 1, [high_byte_val])

    def setPwmOff(self, addr, ch, value):
        low_byte_val  =   value & 0x00FF 
        high_byte_val = ( value & 0x0F00 ) >> 8
        reg_low_byte = 0x08 + 4 * ch
        bus.write_i2c_block_data(addr, reg_low_byte    , [low_byte_val ])
        bus.write_i2c_block_data(addr, reg_low_byte + 1, [high_byte_val])

    def motorRun(self, num, speed ,inverse):
        motorPin = {self.motorSet[0]:[2,3,4],
                    self.motorSet[1]:[7,6,5],
                    self.motorSet[2]:[8,9,10],
                    self.motorSet[3]:[13,12,11]}
        if num not in motorPin : raise IOError('not suppot DC Motor Number(1 to 4)')
        
        #for i in range(0,16):
        self.setPwmOff(pca9685_addr, motorPin[num][0],speed)
        if not inverse:
            self.setPwmOff(pca9685_addr, motorPin[num][1],0)
            self.setPwmOff(pca9685_addr, motorPin[num][2],2048)
        else:
            self.setPwmOff(pca9685_addr, motorPin[num][1],2048)
            self.setPwmOff(pca9685_addr, motorPin[num][2],0)
        
    def carFront(self,speed):
        self.motorRun(1, speed, False)
        self.motorRun(2, speed, False)
        self.motorRun(3, speed, False)
        self.motorRun(4, speed, False)

    def carBack(self,speed):
        self.motorRun(1, speed, True)
        self.motorRun(2, speed, True)
        self.motorRun(3, speed, True)
        self.motorRun(4, speed, True)

    def carRight(self,speed):
        self.motorRun(1, speed, True)
        self.motorRun(2, speed, False)
        self.motorRun(3, speed, True)
        self.motorRun(4, speed, False)

    def carLeft(self,speed):
        self.motorRun(1, speed, False)
        self.motorRun(2, speed, True)
        self.motorRun(3, speed, False)
        self.motorRun(4, speed, True)


    def carLShift(self,speed):
        self.motorRun(1, speed, False)
        self.motorRun(2, speed, True)
        self.motorRun(3, speed, True)
        self.motorRun(4, speed, False)

    def carRShift(self,speed):
        self.motorRun(1, speed, True)
        self.motorRun(2, speed, False)
        self.motorRun(3, speed, False)
        self.motorRun(4, speed, True)

    def carLFOblique(self,speed):
        self.motorRun(1, 0, True)
        self.motorRun(2, speed, False)
        self.motorRun(3, speed, False)
        self.motorRun(4, 0, True)

    def carRFOblique(self,speed):
        self.motorRun(1, speed, False)
        self.motorRun(2, 0, True)
        self.motorRun(3, 0, True)
        self.motorRun(4, speed, False)

    def carLBOblique(self,speed):
        self.motorRun(1, 0, True)
        self.motorRun(2, speed, True)
        self.motorRun(3, speed, True)
        self.motorRun(4, 0, True)

    def carRBOblique(self,speed):
        self.motorRun(1, speed, True)
        self.motorRun(2, 0, True)
        self.motorRun(3, 0, True)
        self.motorRun(4, speed, True)

    def carStop(self,speed):
        self.motorRun(1, 0, False)
        self.motorRun(2, 0, True)
        self.motorRun(3, 0, True)
        self.motorRun(4, 0, False)


if __name__ == '__main__':
    car = DCMotor()
    print('Front')
    car.carFront(700)
    time.sleep(2)

    print('Back')
    car.carBack(700)
    time.sleep(2)

    print('Left')
    car.carLeft(700)
    time.sleep(2)

    print('Right')
    car.carRight(700)
    time.sleep(2)

    print('LShift')
    car.carLShift(700)
    time.sleep(2)

    print('RShift')
    car.carRShift(700)
    time.sleep(2)

    print('carLFOblique')
    car.carLFOblique(700)
    time.sleep(2)

    print('carRFOblique')
    car.carRFOblique(700)
    time.sleep(2)

    print('carLBOblique')
    car.carLBOblique(700)
    time.sleep(2)

    print('carRBOblique')
    car.carRBOblique(700)
    time.sleep(2)

    car.carStop(700)
