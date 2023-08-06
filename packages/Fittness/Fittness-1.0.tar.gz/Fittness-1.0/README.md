# data533Lab4
In the subpackage **calories_burned**, it has two modules, *records* and *monitoring*. *Records* is the super class of *Monitoring* and it has 5 funcitons.

***Records***
1. In the initializing stage. It takes name,gender,age,height,weight as arguments 
2. **Records.display()** takes self as argument and print out the details such as name, gender,age ,height and weight in the initializing stage
3. **Records.BMI()** calculates the body mass index based on generated perosnal information and tells the weight status in the ragne from underweiht to obse.
4. **Records.BMR()** calcualtes the Basal metabolic rate. BMR is a measurement of the number of calories needed to perform a person's most basic funcitons such as breathing. Each gender has different formular to calculate BMR
    - ***Female_bmr= 655 + (9.6 * self.weight) + (1.8* self.height- (4.7* self.age))**
    - ***Male_bmr= 66 + (13.7*self.weight) + (5*self.height) - (6.8*self.age)***
5. **Records.totalcal()** calcuates the total borned calories based on BMR, intensity of excerise and the excerise time.Excersise intensity and time are getting from the user's input, for simlicity reason, intensity has only 3 levels 3(Light),4(Moderate),7(Vigorous) and time is measured in minutes,require BMR to be calcualted.

**Prerequisite**
Have pygal installed
pip install pygal


***Monitoring***
Monitoring is the sub class of Records, It could be used to monitory weight and calory changes in weekly or monthly basis
1. In the initializing stage. It  takes all the arguemtns from Records and an additional new arguments calory 
2. **Monitoring.new_weight(newweight)** append daily weight to weight_list
3. **Monitoring.new_calory(newcalory)** append daily burned calory to calory_list
4. **Monitoring.weight_change_plot()** create a line chart which shows the daily weight and the changes overtime 
5. **Monitoring.calory_change_plot()** create a line chart which shows the daily burned calories and the changes overtime
6. **Monitoring.weight_calory_plot()** create a bar chart that contians both daily weight and burned calory in the same graph  

In the subpackage **calories_burned**, it has two modules, *records* and *monitoring*. *Records* is the super class of *Monitoring* and it has 5 funcitons.

***Records***
1. In the initializing stage. It takes name,gender,age,height,weight as arguments 
2. **Records.display()** takes self as argument and print out the details such as name, gender,age ,height and weight in the initializing stage
3. **Records.BMI()** calculates the body mass index based on generated perosnal information and tells the weight status in the ragne from underweiht to obse.
4. **Records.BMR()** calcualtes the Basal metabolic rate. BMR is a measurement of the number of calories needed to perform a person's most basic funcitons such as breathing. Each gender has different formular to calculate BMR
    - ***Female_bmr= 655 + (9.6 * self.weight) + (1.8* self.height- (4.7* self.age))**
    - ***Male_bmr= 66 + (13.7*self.weight) + (5*self.height) - (6.8*self.age)***
5. **Records.totalcal()** calcuates the total borned calories based on BMR, intensity of excerise and the excerise time.Excersise intensity and time are getting from the user's input, for simlicity reason, intensity has only 3 levels 3(Light),4(Moderate),7(Vigorous) and time is measured in minutes,require BMR to be calcualted.

**Prerequisite**
Have pygal installed
pip install pygal


***Monitoring***
Monitoring is the sub class of Records, It could be used to monitory weight and calory changes in weekly or monthly basis
1. In the initializing stage. It  takes all the arguemtns from Records and an additional new arguments calory 
2. **Monitoring.new_weight(newweight)** append daily weight to weight_list
3. **Monitoring.new_calory(newcalory)** append daily burned calory to calory_list
4. **Monitoring.weight_change_plot()** create a line chart which shows the daily weight and the changes overtime 
5. **Monitoring.calory_change_plot()** create a line chart which shows the daily burned calories and the changes overtime
6. **Monitoring.weight_calory_plot()** create a bar chart that contians both daily weight and burned calory in the same graph  