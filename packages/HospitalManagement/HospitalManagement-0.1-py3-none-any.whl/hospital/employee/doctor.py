class SalaryError(Exception):
    def __init__(self):
        pass
    
class Doctor:
    def __init__(self,name,age,phone_num,salary,number_treated):
        self.name = name
        self.age = age
        self.phone_num = phone_num
        self.salary = salary
        self.number_treated = number_treated

    def change_in_phone_num(self,phone_num):
        self.phone_num = phone_num

    def change_in_salary(self,salary):

        try: 
            if salary < 0:
                raise SalaryError
        except SalaryError:
            return("Invalid salary.")
        else:
            self.salary = salary
    
    def bonus(self):
        bonus = 20 * self.number_treated
        self.salary += bonus
        return("This doctor's bonus salary is {}\nWith bonus salary, the doctor's total salary is {}"
              .format(bonus,self.salary))

    def display(self):
        return ("Dr.{} is {} years old. The best number to reach out is {}. \nThe doctor's base salary is {}. \nThe doctor has treated {} patients.\n".format(self.name,self.age,self.phone_num,self.salary,self.number_treated))
