import pygal
from Fittness.calories_burn import records
from IPython.display import SVG, display


class Monitoring(records.Records):
    """
    Aim to monitory the daily changes of weight and burned calories
    """
    def __init__(self,name,gender,age,height,weight,calories):
        records.Records.__init__(self,name,gender,age,height,weight)

        self.calories=calories
        self.weight_list=[weight]
        self.calories_list=[calories]
        try:
            if self.age<0:
                raise ValueError("please enter a valid age")
        except ValueError as ex:
            print("Message:", ex)

        try:

            if self.height<50 or self.height>210:
                raise ValueError("please enter a valid height in cm")
        except ValueError as ex:
            print("Message:", ex)

        try:
            if self.weight<0:
                raise ValueError("invalid weight")
        except ValueError:
            print("please enter a valid weight")

        try:
            if self.calories<0:
                raise ValueError("invalid calories")
        except ValueError:
            print("please enter a valid invalid calroies")

    
    def new_weight(self,newweight):
        self.weight_list.append(newweight)
        return self.weight_list

    
    def new_calory(self,newcalory):
        self.calories_list.append(newcalory)
        return self.calories_list
    
    def weight_change_plot(self):
        line_chart = pygal.Line()
        line_chart.title = 'Daily weight Changes '
        line_chart.x_title='Day'
        line_chart.y_title='kg'
        line_chart.add(self.name, self.weight_list)
        line_chart.x_labels = map(str, range(0,len(self.weight_list)))
        line_chart.render()
        display(SVG(line_chart.render (disable_xml_declaration=True)))

    def calory_change_plot(self):
        line_chart = pygal.Line()
        line_chart.title = 'Daily Burned Calories '
        line_chart.x_title='Day'
        line_chart.y_title='cal'
        line_chart.add(self.name, self.calories_list)
        line_chart.x_labels = map(str, range(0,len(self.calories_list)))
        line_chart.render()
        display(SVG(line_chart.render (disable_xml_declaration=True)))
    
    def weight_calory_plot(self):
        bar_chart = pygal.Bar() 
        bar_chart.add('calory', self.calories_list) 
        bar_chart.add('weight', self.weight_list)
        bar_chart.render
        display(SVG(bar_chart.render(disable_xml_declaration=True)))


