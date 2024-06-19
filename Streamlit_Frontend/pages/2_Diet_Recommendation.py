import streamlit as st
import pandas as pd
from Generate_Recommendations import Generator
from random import uniform as rnd
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts
import base64

logo = """
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="white"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    class="h-6 w-6"
    >
    <path d="M7 21h10"></path>
    <path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"></path>
    <path
        d="M11.38 12a2.4 2.4 0 0 1-.4-4.77 2.4 2.4 0 0 1 3.2-2.77 2.4 2.4 0 0 1 3.47-.63 2.4 2.4 0 0 1 3.37 3.37 2.4 2.4 0 0 1-1.1 3.7 2.51 2.51 0 0 1 .03 1.1"
    ></path>
    <path d="m13 12 4-4"></path>
    <path
        d="M10.9 7.25A3.99 3.99 0 0 0 4 10c0 .73.2 1.41.54 2"
    ></path>
</svg>
"""

logo_64 = base64.b64encode(logo.encode()).decode()

st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon=f"data:image/svg+xml;base64,{logo_64}",
    layout="wide",
    initial_sidebar_state="expanded",
)

custom_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background: url("https://i.imgur.com/dEM3RFf.jpg");
    background-size: cover;
    height: 100vh;
}

[data-testid="stToolbar"] {
right: 2rem;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}
</style>
"""

# Include custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

nutritions_values = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
                     'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']
# Streamlit states initialization
if 'person' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None
    st.session_state.person = None
    st.session_state.weight_loss_option = None


class Person:

    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss, is_diabetic):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss
        self.is_diabetic = is_diabetic
    def calculate_bmi(self,):
        bmi = round(self.weight/((self.height/100)**2), 2)
        return bmi

    def display_result(self,):
        bmi = self.calculate_bmi()
        bmi_string = f'{bmi} kg/m²'
        if bmi < 18.5:
            category = 'Underweight'
            color = 'Red'
        elif 18.5 <= bmi < 25:
            category = 'Normal'
            color = 'Green'
        elif 25 <= bmi < 30:
            category = 'Overweight'
            color = 'Yellow'
        else:
            category = 'Obesity'
            color = 'Red'
        return bmi_string, category, color

    def calculate_bmr(self):
        if self.gender == 'Male':
            bmr = 10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr = 10*self.weight+6.25*self.height-5*self.age-161
        return bmr

    def calories_calculator(self):
        activites = ['Little/no exercise', 'Light exercise',
                     'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories

    def generate_recommendations(self):
        try:
            total_calories = self.weight_loss * self.calories_calculator()
            recommendations = []
            for meal in self.meals_calories_perc:
                meal_calories = self.meals_calories_perc[meal] * total_calories

                # Default recommended nutrition
                default_nutrition = [meal_calories, rnd(10, 30), rnd(0, 4), rnd(
                    0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 10), rnd(0, 10), rnd(30, 100)]

                if self.is_diabetic:
                    # Diabetic-friendly recommendations
                    if meal == 'breakfast':
                        recommended_nutrition = [meal_calories, rnd(10, 20), rnd(0, 2), rnd(
                            0, 15), rnd(0, 200), rnd(20, 45), rnd(2, 5), rnd(0, 5), rnd(10, 50)]
                    elif meal == 'lunch':
                        recommended_nutrition = [meal_calories, rnd(20, 30), rnd(0, 2), rnd(
                            0, 15), rnd(0, 200), rnd(20, 45), rnd(2, 5), rnd(0, 5), rnd(10, 50)]
                    elif meal == 'dinner':
                        recommended_nutrition = [meal_calories, rnd(20, 30), rnd(0, 2), rnd(
                            0, 15), rnd(0, 200), rnd(20, 45), rnd(2, 5), rnd(0, 5), rnd(10, 50)]
                    else:
                        recommended_nutrition = default_nutrition
                else:
                    # Regular recommendations
                    recommended_nutrition = default_nutrition

                generator = Generator(recommended_nutrition, is_diabetic=self.is_diabetic)
                recommended_recipes = generator.generate().json()

                # Debugging statements
                print("Recommended Recipes:", recommended_recipes)

                output = recommended_recipes.get('output')
                if output is not None:
                    recommendations.append(output)
                else:
                    print("Error: 'output' key not found in the response.")


            for recommendation in recommendations:
                for recipe in recommendation:
                    recipe['image_link'] = find_image(recipe['Name'])

            return recommendations

        except Exception as e:
            print(f"Error in generate_recommendations: {e}")
            return None


class Display:
    def __init__(self):
        self.plans = ["Maintain weight", "Mild weight loss",
                      "Weight loss", "Extreme weight loss"]
        self.weights = [1, 0.9, 0.8, 0.6]
        self.losses = ['-0 kg/week', '-0.25 kg/week',
                       '-0.5 kg/week', '-1 kg/week']
        pass

    def display_bmi(self, person):
        st.header('BMI CALCULATOR')
        bmi_string, category, color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            Healthy BMI range: 18.5 kg/m² - 25 kg/m².
            """)

    def display_calories(self, person):
        st.header('CALORIES CALCULATOR')
        maintain_calories = person.calories_calculator()
        st.write('The results show a number of daily calorie estimates that can be used as a guideline for how many calories to consume each day to maintain, lose, or gain weight at a chosen rate.')
        for plan, weight, loss, col in zip(self.plans, self.weights, self.losses, st.columns(4)):
            with col:
                st.metric(
                    label=plan, value=f'{round(maintain_calories*weight)} Calories/day', delta=loss, delta_color="inverse")

    def display_recommendation(self, person, recommendations):
        st.header('DIET RECOMMENDATOR')
        with st.spinner('Generating recommendations...'):
            meals = person.meals_calories_perc
            st.subheader('Recommended recipes:')
            for meal_name, column, recommendation in zip(meals, st.columns(len(meals)), recommendations):
                with column:
                    # st.markdown(f'<div style="text-align: center;">{meal_name.upper()}</div>', unsafe_allow_html=True)
                    st.markdown(f'##### {meal_name.upper()}')
                    for recipe in recommendation:

                        recipe_name = recipe['Name']
                        expander = st.expander(recipe_name)
                        recipe_link = recipe['image_link']
                        recipe_img = f'<div><center><img src={recipe_link} alt={recipe_name}></center></div>'
                        nutritions_df = pd.DataFrame(
                            {value: [recipe[value]] for value in nutritions_values})

                        expander.markdown(recipe_img, unsafe_allow_html=True)
                        expander.markdown(
                            f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values (g):</h5>', unsafe_allow_html=True)
                        expander.dataframe(nutritions_df)
                        expander.markdown(
                            f'<h5 style="text-align: center;font-family:sans-serif;">Ingredients:</h5>', unsafe_allow_html=True)
                        for ingredient in recipe['RecipeIngredientParts']:
                            expander.markdown(f"""
                                        - {ingredient}
                            """)
                        expander.markdown(
                            f'<h5 style="text-align: center;font-family:sans-serif;">Recipe Instructions:</h5>', unsafe_allow_html=True)
                        for instruction in recipe['RecipeInstructions']:
                            expander.markdown(f"""
                                        - {instruction}
                            """)
                        expander.markdown(
                            f'<h5 style="text-align: center;font-family:sans-serif;">Cooking and Preparation Time:</h5>', unsafe_allow_html=True)
                        expander.markdown(f"""
                                - Cook Time       : {recipe['CookTime']}min
                                - Preparation Time: {recipe['PrepTime']}min
                                - Total Time      : {recipe['TotalTime']}min
                            """)

    def display_meal_choices(self, person, recommendations):
        st.subheader('Choose your meal composition:')
        # Display meal compositions choices
        if not recommendations or len(recommendations) < 3:
            st.warning("Not enough recommendations to display.")
            return

        if len(recommendations) == 3:
            breakfast_column, launch_column, dinner_column = st.columns(3)
            with breakfast_column:
                breakfast_choice = st.selectbox(f'Choose your breakfast:', [
                                                recipe['Name'] for recipe in recommendations[0]])
            with launch_column:
                launch_choice = st.selectbox(f'Choose your launch:', [
                                             recipe['Name'] for recipe in recommendations[1]])
            with dinner_column:
                dinner_choice = st.selectbox(f'Choose your dinner:', [
                                             recipe['Name'] for recipe in recommendations[2]])
            choices = [breakfast_choice, launch_choice, dinner_choice]
        elif len(recommendations) == 4:
            breakfast_column, morning_snack, launch_column, dinner_column = st.columns(
                4)
            with breakfast_column:
                breakfast_choice = st.selectbox(f'Choose your breakfast:', [
                                                recipe['Name'] for recipe in recommendations[0]])
            with morning_snack:
                morning_snack = st.selectbox(f'Choose your morning_snack:', [
                                             recipe['Name'] for recipe in recommendations[1]])
            with launch_column:
                launch_choice = st.selectbox(f'Choose your launch:', [
                                             recipe['Name'] for recipe in recommendations[2]])
            with dinner_column:
                dinner_choice = st.selectbox(f'Choose your dinner:', [
                                             recipe['Name'] for recipe in recommendations[3]])
            choices = [breakfast_choice, morning_snack,
                       launch_choice, dinner_choice]
        else:
            breakfast_column, morning_snack, launch_column, afternoon_snack, dinner_column = st.columns(
                5)
            with breakfast_column:
                breakfast_choice = st.selectbox(f'Choose your breakfast:', [
                                                recipe['Name'] for recipe in recommendations[0]])
            with morning_snack:
                morning_snack = st.selectbox(f'Choose your morning_snack:', [
                                             recipe['Name'] for recipe in recommendations[1]])
            with launch_column:
                launch_choice = st.selectbox(f'Choose your launch:', [
                                             recipe['Name'] for recipe in recommendations[2]])
            with afternoon_snack:
                afternoon_snack = st.selectbox(f'Choose your afternoon:', [
                                               recipe['Name'] for recipe in recommendations[3]])
            with dinner_column:
                dinner_choice = st.selectbox(f'Choose your  dinner:', [
                                             recipe['Name'] for recipe in recommendations[4]])
            choices = [breakfast_choice, morning_snack,
                       launch_choice, afternoon_snack, dinner_choice]

        # Calculating the sum of nutritional values of the choosen recipes
        total_nutrition_values = {
            nutrition_value: 0 for nutrition_value in nutritions_values}
        for choice, meals_ in zip(choices, recommendations):
            for meal in meals_:
                if meal['Name'] == choice:
                    for nutrition_value in nutritions_values:
                        total_nutrition_values[nutrition_value] += meal[nutrition_value]

        total_calories_chose = total_nutrition_values['Calories']
        loss_calories_chose = round(
            person.calories_calculator()*person.weight_loss)

        # Display corresponding graphs
        st.markdown(
            f'<h5 style="text-align: center;font-family:sans-serif;">Total Calories in Recipes vs {st.session_state.weight_loss_option} Calories:</h5>', unsafe_allow_html=True)
        total_calories_graph_options = {
            "xAxis": {
                "type": "category",
                "data": ['Total Calories you chose', f"{st.session_state.weight_loss_option} Calories"],
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "data": [
                        {"value": total_calories_chose, "itemStyle": {
                            "color": ["#33FF8D", "#FF3333"][total_calories_chose > loss_calories_chose]}},
                        {"value": loss_calories_chose,
                            "itemStyle": {"color": "#3339FF"}},
                    ],
                    "type": "bar",
                }
            ],
        }
        st_echarts(options=total_calories_graph_options, height="400px",)
        st.markdown(
            f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>', unsafe_allow_html=True)
        nutritions_graph_options = {
            "tooltip": {"trigger": "item"},
            "legend": {"top": "5%", "left": "center"},
            "series": [
                {
                    "name": "Nutritional Values",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 10,
                        "borderColor": "#fff",
                        "borderWidth": 2,
                    },
                    "label": {"show": False, "position": "center"},
                    "emphasis": {
                        "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                    },
                    "labelLine": {"show": False},
                    "data": [{"value": round(total_nutrition_values[total_nutrition_value]), "name":total_nutrition_value} for total_nutrition_value in total_nutrition_values],
                }
            ],
        }
        st_echarts(options=nutritions_graph_options, height="500px",)


display = Display()
title = "<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)
with st.form("recommendation_form"):
    st.write("Modify the values and click the Generate button to use")
    age = st.number_input('Age', min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)', min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)', min_value=10, max_value=300, step=1)
    gender = st.radio('Gender', ('Male', 'Female'))
    activity = st.select_slider('Activity', options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)',
                                                     'Extra active (very active & physical job)'])
    option = st.selectbox('Choose your weight loss plan:', display.plans)
    st.session_state.weight_loss_option = option
    weight_loss = display.weights[display.plans.index(option)]
    number_of_meals = st.slider(
        'Meals per day', min_value=3, max_value=5, step=1, value=3)
    is_diabetic = st.radio("Do you have diabetes?", ("Yes", "No"))
    if number_of_meals == 3:
        meals_calories_perc = {'breakfast': 0.35,
                               'lunch': 0.40, 'dinner': 0.25}
    elif number_of_meals == 4:
        meals_calories_perc = {
            'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'dinner': 0.25}
    else:
        meals_calories_perc = {'breakfast': 0.30, 'morning snack': 0.05,
                               'lunch': 0.40, 'afternoon snack': 0.05, 'dinner': 0.20}
    generated = st.form_submit_button("Generate")
if generated:
    is_diabetic = True if is_diabetic == "Yes" else False
    st.session_state.generated = True
    person = Person(age, height, weight, gender, activity,
                    meals_calories_perc, weight_loss, is_diabetic)
    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)
    with st.spinner('Generating recommendations...'):
        recommendations = person.generate_recommendations()
        st.session_state.recommendations = recommendations
        st.session_state.person = person

if st.session_state.generated:
    with st.container():
        display.display_recommendation(
            st.session_state.person, st.session_state.recommendations)
        st.success('Recommendation Generated Successfully !', icon="✅")
    with st.container():
        display.display_meal_choices(
            st.session_state.person, st.session_state.recommendations)
