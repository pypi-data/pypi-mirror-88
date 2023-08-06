
class Records:
    """
    please enter your name, age,height in cm and weight in kg
    """

    def __init__(self,name,gender,age,height,weight):
        self.gender=gender
        self.height=height  
        self.weight=weight 
        self.name=name
        self.age=age
        self.bmi_range="n"
        try:
            if self.age<0:
                raise ValueError("please enter a valid age")
        except ValueError as ex:
            print("Message:", ex)

        # try:
        #     if self.gender!="female" or self.gender!="male":
        #         raise ValueError("plase enter your gender, male or female")
        # except ValueError as ex:
        #     print("Message:", ex)
            
        try:

            if self.height<50 or self.height>210:
                raise ValueError("please enter a valid height in cm")
        except ValueError as ex:
            print("Message:", ex)
        
        try:
            if self.weight<10 or self.weight>300:
                raise ValueError("please enter a valid weight in kg")

        except ValueError as ex:
            print("Message:", ex)


            


            





    




    def display(self):
        return "Name: {} Age: {} Gender:{} Height: {}cm Wegiht: {}kg".format(self.name,self.age,self.gender,self.height,self.weight)
     
        
    def BMI(self):
        """""
        https://www.cdc.gov/obesity/adult/defining.html#:~:text=If%20your%20BMI%20is%20less,falls%20within%20the%20obese%20range.
        BMI=body mass index
        m=mass (in kilograms)
        h=height (height (in meters))
        """
        bmi=self.weight/(self.height/100)**2
        if bmi<18.5:
            self.bmi_range="underweight"
        elif bmi>18.5 and bmi<25:
            self.bmi_range="normal"
        elif bmi>25 and bmi<30:
            self.bmi_range="overweight"
        elif bmi>30:
            self.bmi_range="obese"
        self.bmi=bmi    
        return "Hello,{} your BMI is {:0.2f} which is in {} range".format(self.name,bmi,self.bmi_range)
        
    def BMR(self):
        """
        Basal metabolic rate is a measurement 
        of the number of calories needed to perform 
        your body's most basic (basal) functions, 
        like breathing, circulation and cell production. 
        BMR is most accurately measured in a lab setting under very restrictive conditions
        """
        """
        https://www.bmi-calculator.net/bmr-calculator/bmr-formula.php
        Harris-Benedict Equation
        Women: BMR = 655 + (9.6 x weight in kg) + (1.8 x height in cm) - (4.7 x age in years)
        Men: BMR = 66 + (13.7 x weight in kg) + (5 x height in cm) - (6.8 x age in years)
        """
        if self.gender=="female":
            bmr= 655 + (9.6 * self.weight) + (1.8* self.height- (4.7* self.age))
        else:
            bmr= 66 + (13.7*self.weight) + (5*self.height) - (6.8*self.age)
        self.bmr=bmr
        return "Hello,{} your BMR is around {} Kcal/day".format(self.name,bmr)
     
    
    def totalcal(self):
        """
        time= exercise time (in mintues)
        intensity has three levels= 3(Light),4(Moderate),7(Vigorous)
        Total calories burned = Duration (in minutes)*(MET*3.5*weight in kg)/200. 
        """
        x=1
        while x!=0:
            y=input("Did you do any exercises today (Yes/No): ")
            if y== "Yes":
                intensity=int(input("Intensity has three levels= 3(Light),4(Moderate),7(Vigorous) please enter your level: "))
                time=int(input("Please Enter exercise time in minutes:  "))
                x=0

            if y=="No":
                intensity=0
                time=0
                x=0
        
            else:
                print("please check your answer, please either enter Yes or No" )

        exc_cal=time*(intensity*3.5*self.weight)/200
        total=round(exc_cal+self.bmr)
        print("Hello,the total burned calories for today is {} cal".format(total))
        return total


