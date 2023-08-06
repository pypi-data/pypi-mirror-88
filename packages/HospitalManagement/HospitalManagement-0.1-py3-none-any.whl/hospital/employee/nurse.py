class SalaryError(Exception):
    def __init__(self):
        pass
class Nurse:
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
            return "Invalid salary."
        else:
            self.salary = salary
    
    def bonus(self):
        bonus = 10 * self.number_treated
        self.salary += bonus
        print("This nurse's bonus salary is {}\nWith bonus salary, the nurse's total salary is {}"
              .format(bonus,self.salary))

    def display(self):
        return("Nurse {} is {} years old. \nThe best number to reach out is {}. \nThe nurse's salary is {}. \nThe nurse has treated {} patients.\n".format(self.name,self.age,self.phone_num,self.salary,self.number_treated))
