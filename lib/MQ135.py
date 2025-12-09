from math import pow
from machine import ADC, Pin

class MQ135(ADC):

    # The load resistance on the board
    RLOAD = 10.0
    # Calibration resistance at atmospheric CO2 level
    RZERO = 4.029679
    # Parameters for calculating ppm of CO2 from sensor resistance
    PARA = 116.6020682
    PARB = 2.769034857

    # Parameters to model temperature and humidity dependence
    CORA = 0.00035
    CORB = 0.02718
    CORC = 1.39538
    CORD = 0.0018

    # Atmospheric CO2 level for calibration purposes
    ATMOCO2 = 397.13


    ## @brief  Default constructor
    ## @param[in] pin  The analog input pin for the readout of the sensor
   
    def __init__(self, pin) :
        super().__init__(Pin(pin))
        #self._pin = pin #TODO to change
    


 
    ## @brief  Get the correction factor to correct for temperature and humidity
    ## @param[in] t  The ambient air temperature
    ## @param[in] h  The relative humidity
    ## @return The calculated correction factor
  
    def getCorrectionFactor(self, t, h) :
      return self.CORA*t*t - self.CORB*t + self.CORC - (h-33.)*self.CORD
    

 
    ## @brief  Get the resistance of the sensor, ie. the measurement value
    ## @return The sensor resistance in kOhm

    def getResistance(self) :
        val = self.read();   #TODO change using ADC
        return ((1023./val) * 5. - 1.)*self.RLOAD
    

    
    ## @brief  Get the resistance of the sensor, ie. the measurement value corrected for temp/hum
    ## @param[in] t  The ambient air temperature
    ## @param[in] h  The relative humidity
    ## @return The corrected sensor resistance kOhm
    
    def getCorrectedResistance(self, t, h) :
        return self.getResistance()/self.getCorrectionFactor(t, h)
    

    
    ## @brief  Get the ppm of CO2 sensed (assuming only CO2 in the air)
    ## @return The ppm of CO2 in the air
    
    def getPPM(self) :
        return self.PARA * pow((self.getResistance()/self.RZERO), -self.PARB) 
    


    ## @brief  Get the ppm of CO2 sensed (assuming only CO2 in the air), corrected for temp/hum
    ## @param[in] t  The ambient air temperature
    ## @param[in] h  The relative humidity
    ## @return The ppm of CO2 in the air

    def getCorrectedPPM(self, t, h) :
        return self.PARA * pow((self.getCorrectedResistance(t, h)/self.RZERO), -self.PARB) 
    


    ## @brief  Get the resistance RZero of the sensor for calibration purposes
    ## @return The sensor resistance RZero in kOhm
    
    def getRZero(self) :
        return self.getResistance() * pow((self.ATMOCO2/self.PARA), (1./self.PARB))
    

    
    ## @brief  Get the corrected resistance RZero of the sensor for calibration purposes
    ## @param[in] t  The ambient air temperature
    ## @param[in] h  The relative humidity
    ## @return The corrected sensor resistance RZero in kOhm
    
    def getCorrectedRZero(self, t, h) :
        RZERO = self.getCorrectedResistance(t, h) * pow((self.ATMOCO2/self.PARA), (1./self.PARB))
        return RZERO
    
def demo():
    MyMQ = MQ135(2)
    a = MyMQ.getCorrectedPPM(1,2)
    print(a)
    
if __name__ == "__main__" :
    # Code that runs only if this script is executed directly
    demo()
     

