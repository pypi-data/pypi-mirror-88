class Nutrients:
    
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def display(self):
        print('You have consumed {:.2f} grams {} today.'.format(self.amount, self.name))


class Protein(Nutrients):
    
    def __init__(self, name, amount, calPerGram=4):
        Nutrients.__init__(self, name, amount)
        self.calPerGram = calPerGram
        
    def protCal(self):
        return self.amount * self.calPerGram
        
    def displaypCalories(self):
        Nutrients.display(self)
        toAmount = self.amount * self.calPerGram
        print('Calories intaken from protein is {:.2f}.'.format(toAmount))


class Fat(Nutrients):
    
    def __init__(self, name, amount, calPerGram=9):
        Nutrients.__init__(self, name, amount)
        self.calPerGram = calPerGram
        
    def fatCal(self):
        return self.amount * self.calPerGram
        
    def displayfCalories(self):
        Nutrients.display(self)
        toAmount = self.amount * self.calPerGram
        print('Calories intaken from fat is {:.2f}.'.format(toAmount))


class Carbohydrate(Nutrients):
    
    def __init__(self, name, amount, calPerGram=4):
        Nutrients.__init__(self, name, amount)
        self.calPerGram = calPerGram
        
    def carbCal(self):
        return self.amount * self.calPerGram
        
    def displaycCalories(self):
        Nutrients.display(self)
        toAmount = self.amount * self.calPerGram
        print('Calories intaken from carbohydrate is {:.2f}.'.format(toAmount))

        
class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return(repr(self.value))
    
    
def entry():
    
    """
    This function is for the user to enter information to each specific question
    in order to obtain nutritional and dietary related summary.
    
    """
    
    try:
        proteinIntake = float(input('How many protein have you consumed in gram?'))
        if proteinIntake > 1000 or proteinIntake < 10:
            raise InputError(proteinIntake)
        fatIntake = float(input('How many fat have you consumed in gram?'))
        if fatIntake > 1000 or fatIntake < 10:
            raise InputError(fatIntake)
        carbIntake = float(input('How many carbohydrate have you consumed in gram?'))
        if carbIntake > 1000 or carbIntake < 10:
            raise InputError(carbIntake)
        
        weight = float(input('What is your weight in kg?'))
        if weight > 500 or weight <= 0:
            raise InputError(weight)
        height = float(input('What is your height in cm?'))
        if height > 250 or height <= 0:
            raise InputError(height)
        age = int(input('What is your current age?'))
        if age > 150 or age < 0:
            raise InputError(age)
        sex = input('What is your gender? (m/f)')
        if sex not in ['m', 'f']:
            raise InputError(sex)
        
    except InputError as ex:
        print('Exception raised:', ex.value, 'is out of the range')
    except ValueError as ex:
        print('Please enter a valid value')
    except:
        print('There is an error')
        
    print('Choose your activity level:')
    print('1 - Sedentary (little or no exercise)')
    print('2 - Lightly active (exercise 1-3 days/week)')
    print('3 - Moderately active (exercise 3-5 days/week)')
    print('4 - Active (exercise 6-7 days/week)')
    print('5 - Very active (hard exercise 6-7 days/week)')
    answer = input()
    if answer == '1':
        act_fact = 1.26
        
    elif answer == '2':
        act_fact = 1.375
    elif answer == '3':
        act_fact = 1.55
    elif answer == '4':
        act_fact = 1.725
    elif answer == '5':
        act_fact = 1.9
    else:
        raise ValueError('Please choose a valid number')
        
    calCalories(proteinIntake, fatIntake, carbIntake)
    bodyNeeds(weight, height, sex, age, proteinIntake, fatIntake, carbIntake, act_fact)
    
    
def calCalories(protI, fatI, carbI):
    
    """
    Description of the Function

    Parameters:
    protI (float): protein intake in gram provided by the user
    fatI (float): fat intake in gram provided by the user
    carbI (float): carbohydrate intake in gram provided by the user

    Returns:
    print the total calories from all three nutrients intake provided by the user
    
    """
    
    try:
        prot = Protein('protein', protI, 4)
        if isinstance(protI, str):
            raise ValueError('It is not a numeric value')
        fat = Fat('fat', fatI, 9)
        if isinstance(fatI, str):
            raise ValueError('It is not a numeric value')
        carb = Carbohydrate('carbohydrate', carbI, 4)
        if isinstance(carbI, str):
            raise ValueError('It is not a numeric value')
    
    except ValueError as ex:
        print('Value Error:', ex)
    except:
        print('There is an error')
        
#     print('Summary:')
#     prot.displaypCalories()
#     fat.displayfCalories()
#     carb.displaycCalories()
    totalCalo = prot.protCal() + fat.fatCal() + carb.carbCal()
    return totalCalo
    
def bodyNeeds(w, h, s, age, proAmt, fatAmt, carbAmt, fac):
    
    """
    Description of the Function

    Parameters:
    w (float): weight in ky provided by the user
    h (float): height in cm provided by the user
    s (string): sex (male/female) provided by the user
    age (int): age provided by the user
    proAmt (float): protein intake in gram provided by the user
    fatAmt (float): fat intake in gram provided by the user
    carbAmt (float): carbohydrate intake in gram provided by the user
    fac (float): activity factor obtained based on the activity level provided by the user

    Returns:
    print the summaries and suggestions for different nutrients intake, as well as
    for total calorie intake based on activity level and dietray intake
    
    """
    
    try:
        prot = Protein('protein', proAmt, 4)
        if isinstance(proAmt, str):
            raise ValueError('It is not a numeric value')
        fat = Fat('fat', fatAmt, 9)
        if isinstance(fatAmt, str):
            raise ValueError('It is not a numeric value')
        carb = Carbohydrate('carbohydrate', carbAmt, 4)
        if isinstance(carbAmt, str):
            raise ValueError('It is not a numeric value')
        totalCalo = prot.protCal() + fat.fatCal() + carb.carbCal()
        rdaPro = 0.8 * w
        rdaFat = 0.3 * totalCalo
        rdaCarb = 0.65 * totalCalo

        if s not in ['f', 'm']:
            raise InputError(s)
        elif s == 'f':
            bmr = (447.6 + 9.25 * w) + (3.10 * h) - (4.33 * age)
            amr = round(bmr * fac, 0)
        elif s == 'm':
            bmr = (88.4 + 13.4 * w) + (4.8 * h) - (5.68 * age)
            amr = round(bmr * fac, 0)
            
        if prot.amount < rdaPro:
            diffP = rdaPro - prot.protCal()
            print('You need to intake {:.2f} more calorie from protein!'.format(diffP))
        if fat.amount > rdaFat:
            diffF = fat.amount - rdaFat
            print('You need to cut your daily fat intake by {:.2f} grams!'.format(diffF))
        elif fat.amount < rdaFat and totalCalo <= bmr:
            diffF = rdaFat - fat.amount
            print('You need to intake {:.2f} more calorie from fat!'.format(diffF))
        if carb.amount > rdaCarb:
            diffC = carb.amount - rdaCarb
            print('You need to cut your daily carbohydrate intake by {:.2f} grams!'.format(diffC))
        elif carb.amount < 0.45 * totalCalo and totalCalo <= bmr:
            diffC = rdaCarb - carb.amount
            print('You need to intake {:.2f} more calorie from carbohydrate!'.format(diffC))
            
        if totalCalo > amr:
            diffCal = totalCalo - amr
            return 'You need to cut down your daily calorie intake or do more exercise!'
        elif totalCalo == amr:
            return 'You are doing great to maintain your weight!'
        else:
            diffCal = amr - totalCalo
            return 'You need to intake more calories daily!'

            
    except InputError as ex:
        print('Exception raised:', ex.value, 'is out of the range')
    except ValueError as ex:
        print('Value Error:', ex)
    except:
        print('There is an error') 