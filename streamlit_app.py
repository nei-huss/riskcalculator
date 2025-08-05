import streamlit as st
import io

# ---- Page Setup ----
st.set_page_config(page_title="Obesity Risk Score Calculator", layout="centered")

# ---- Custom Styling ----
st.markdown("""
    <style>
    .subtitle {
        font-size: 20px;
        font-weight: 600;
        margin: 1.5rem 0 0.75rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Obesity Risk Score Calculator")
st.caption("Understand your weight category and get personalized health insights.")

# ---- Input Fields (Stacked with Default Placeholder) ----
age = st.selectbox("Age", ["Select..."] + list(range(20, 60)))
gender = st.selectbox("Gender", ["Select...", "Male", "Female", "Other"])
height_ft = st.selectbox("Height (feet)", ["Select..."] + list(range(4, 7)))
height_in = st.selectbox("Height (inches)", ["Select..."] + list(range(0, 12)))
weight_lbs = st.selectbox("Weight (lbs)", ["Select..."] + list(range(90, 351)))

# ---- Input Validation ----
if "Select..." in [age, gender, height_ft, height_in, weight_lbs]:
    st.warning("Please fill out all fields above to calculate your BMI.")
    st.stop()

# ---- Health Conditions ----
st.markdown('<div class="subtitle">Health Conditions (Select all that apply)</div>', unsafe_allow_html=True)
has_hypertension = st.checkbox("High blood pressure (hypertension)")
has_diabetes = st.checkbox("Type 2 diabetes")
is_smoker = st.checkbox("Smoker (current or recent)")

# ---- BMI Calculation ----
st.markdown("---")
st.subheader("🔍 Results")

total_height_in = (height_ft * 12) + height_in
bmi = round((weight_lbs / (total_height_in ** 2)) * 703)

if bmi < 18.5:
    bmi_category = "Underweight"
elif 18.5 <= bmi < 25:
    bmi_category = "Healthy weight"
elif 25 <= bmi < 30:
    bmi_category = "Overweight"
elif 30 <= bmi < 35:
    bmi_category = "Obese (Class I)"
elif 35 <= bmi < 40:
    bmi_category = "Obese (Class II)"
else:
    bmi_category = "Severe Obesity (Class III)"

st.metric("Your BMI", f"{bmi}")
st.write(f"**Weight Category:** {bmi_category}")

# ---- BMI-Based Health Insight ----
bmi_insights = {
    "Underweight": "You may be at risk of nutritional deficiencies. Consider consulting a provider.",
    "Healthy weight": "You're in a healthy range. Keep up the good habits!",
    "Overweight": "You may benefit from increased physical activity and mindful eating.",
    "Obese (Class I)": "Your weight may be increasing health risks. Consider professional guidance.",
    "Obese (Class II)": "There's a higher risk of chronic conditions. It's important to take action.",
    "Severe Obesity (Class III)": "Significant health risks are present. Seek medical support to manage weight safely."
}

bmi_actions = {
    "Underweight": [
        "Eat nutrient-rich meals with healthy fats and protein.",
        "Track your weight and consult a provider for underlying causes."
    ],
    "Healthy weight": [
        "Exercise for about 30 minutes a day, 5 days a week.",
        "Monitor your BMI, waist size, and blood pressure once a year."
    ],
    "Overweight": [
        "Minimize added sugars by choosing water over soft drinks and sweetened juices.",
        "Daily walking (30 minutes) contributes to improved metabolic and heart health.",
        "Clinically recommended: aim to lose 5–10% of body weight within 3–6 months to improve health markers."
    ],
    "Obese (Class I)": [
        "Start meal prepping and increase physical activity to 3x/week.",
        "Consult your doctor about a structured weight management plan."
    ],
    "Obese (Class II)": [
        "Adopt a consistent daily routine for meals and activity.",
        "Track glucose, blood pressure, and cholesterol regularly."
    ],
    "Severe Obesity (Class III)": [
        "Consult a medical provider about weight loss options.",
        "Consider clinical programs or support groups for ongoing help."
    ]
}

st.info(bmi_insights.get(bmi_category, "Consult a healthcare provider for personalized advice."))
st.markdown("---")
st.markdown("#### 🎯 Recommended Next Steps")
for tip in bmi_actions.get(bmi_category, []):
    st.write(f"- {tip}")

# ---- Condition-Based Recommendations ----
condition_advice = []

if has_hypertension:
    condition_advice.append("Because you have high blood pressure, even a 5–10% weight loss can lower your BP. Reduce sodium, get regular exercise, and track your blood pressure.")

if has_diabetes:
    condition_advice.append("Managing your weight is key for blood sugar control. Increase fiber intake, cut down refined carbs, and monitor glucose regularly.")

if is_smoker:
    condition_advice.append("Quitting smoking improves health. If you’ve recently quit, stay active and choose whole foods to manage post-quit weight gain.")

if condition_advice:
    st.markdown("#### 🧬 Condition-Specific Guidance")
    for note in condition_advice:
        st.write(f"- {note}")

# ---- Save/Share ----
st.markdown("---")
st.markdown("#### 🔐 Save Your Results")

# Build a summary string
summary = f"""Obesity Risk Score Summary

Age: {age}
Gender: {gender}
Height: {height_ft} ft {height_in} in
Weight: {weight_lbs} lbs

BMI: {bmi}
Weight Category: {bmi_category}

Health Insights:
- {bmi_insights.get(bmi_category, '')}

Lifestyle Tips:
"""
for tip in bmi_actions.get(bmi_category, []):
    summary += f"- {tip}\n"

if condition_advice:
    summary += "\nCondition-Specific Guidance:\n"
    for note in condition_advice:
        summary += f"- {note}\n"

# Download as .txt
buffer = io.StringIO()
buffer.write(summary)
st.download_button(
    label="Download Results Here",
    data=buffer.getvalue(),
    file_name="obesity_risk_score.txt",
    mime="text/plain"
)