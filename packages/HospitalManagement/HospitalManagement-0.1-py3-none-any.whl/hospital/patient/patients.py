class NotValidValue(Exception):
    def __init__ (self):
        pass
    def display(self):
        return "Please enter a list or string."

class GeneralPatient:
    def __init__(self, name, age, date, height, weight, symptom):
        self.age = age
        self.name = name
        self.date = date
        self.height = height
        self.weight = weight
        if type(symptom) == list:
            self.symptom = symptom
        else:
            self.symptom = [symptom]
        self.doc_approve = False
    
    def display(self):
        return "Patient name: {}\nPatient age: {}\nIn hospital date: {}\nSymptoms: {}".format(self.name,
                      self.age,
                      self.date,
                      self.symptom)
    
    def bmi(self):
        try:
            self.weight/(self.height**2)
        except:
            return "Cannot apply since one or both of weight and height is not a number."
        else:
            return "Patient BMI is {}".format(self.weight/(self.height**2))
        
    def full_recovered(self):
        if self.doc_approve == True:
            return "Yes, this patient is ready to leave the hospital."
        else:
            return "No, this patient is not ready to leave the hospital."
        
    def addition_symptom(self, new_symptoms):
        try:
            if type(new_symptoms) == list:
                for i in new_symptoms:
                    self.symptom.append(i)
            elif type(new_symptoms) == str:
                self.symptom.append(new_symptoms)
            else:
                raise NotValidValue
        except NotValidValue as nvv:
            return nvv.display()

    def recovered_symptom(self, rec_symptoms):
        try:
            if type(rec_symptoms) == list:
                for i in rec_symptoms:
                    self.symptom.remove(i)
            elif type(rec_symptoms) == str:
                self.symptom.remove(rec_symptoms)
            else:
                raise NotValidValue
        except ValueError:
            return "Symptom is not in the list, please provide symptoms from existed list."
        except NotValidValue as nvv:
            return nvv.display()
        else:
            if not self.symptom:
                self.doc_approve = True
                return "This patient has been recorvered already, please check condition to leave."

