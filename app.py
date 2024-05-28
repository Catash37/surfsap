pip install -r requirements.txt

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Define the form
class SurfboardForm(FlaskForm):
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    skill_level = SelectField('Skill Level', choices=[
        ('beginner', 'Beginner'),
        ('progressive', 'Progressive'),
        ('advanced', 'Advanced'),
    ], validators=[DataRequired()])
    tail_shape = SelectField('What do you want from your surfboard?', choices=[
        ('allround', 'All Rounder'),
        ('control', 'More Control'),
        ('big', 'Big Waves'),
        ('small', 'Small Waves'),
    ], validators=[DataRequired()])

# Define the route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SurfboardForm()
    if form.validate_on_submit():
        weight = form.weight.data
        skill_level = form.skill_level.data
        tail_shape = form.tail_shape.data
        
        # Calculate volume based on weight and skill level
        skill_levels = {
            'beginner': 0.70,
            'progressive': 0.55,
            'advanced': 0.4,
        }
        skill_factor = skill_levels.get(skill_level, 1.0)
        original_volume = weight * skill_factor
        volume_lower = original_volume - 2
        volume_upper = original_volume + 8
        
        # Define tail shapes information
        tail_shapes_info = {
            'allround': 'Squash tail: Great for all-around performance.',
            'control': 'Round tail: Offers smooth turns and better control.',
            'big': 'Pin tail: Ideal for big waves, provides excellent hold.',
            'small': 'Swallow tail: Enhances maneuverability in small waves.'
        }
        tail_info = tail_shapes_info.get(tail_shape, 'Unknown tail shape')

        return render_template('result.html', volume_lower=volume_lower, volume_upper=volume_upper, tail_info=tail_info)
    return render_template('calculate.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
