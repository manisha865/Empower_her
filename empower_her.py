import hashlib
import random
import smtplib
import streamlit as st
from pymongo import MongoClient
import datetime

# Email Configuration
EMAIL_ADDRESS = "empowerher12345@gmail.com"
EMAIL_PASSWORD = "nwft qatt xqdx kpgi"

# MongoDB Setup

CONNECTION_STRING = "mongodb+srv://manisha:<manisha>@empowerher.fpkmk.mongodb.net/?retryWrites=true&w=majority&appName=empowerher"

# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)
db = client.get_database("empowerher")  # Replace with your database name
users_collection = db.get_collection("users")  # Replace with your collection name

# Helper Functions
def hash_password(password):
    """Hashes the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def send_otp(email):
    """Generates and sends OTP to the given email address."""
    otp = random.randint(100000, 999999)
    try:
        # Connecting to the SMTP server and sending the OTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f"Subject: Your OTP Code\n\nYour OTP code is: {otp}"
            server.sendmail(EMAIL_ADDRESS, email, message)
            return otp  # Return OTP if successfully sent
    except smtplib.SMTPException as e:
        st.error(f"Failed to send OTP due to SMTP error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Login function with OTP verification
def login():
    """Handles the login process with OTP verification."""
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Request OTP"):
        # Check if the username and password are correct
        user = users_collection.find_one({"username": username})
        if user and user["password"] == hash_password(password):
            otp = send_otp(user["email"])  # Send OTP to the user's email
            if otp:
                st.session_state["otp"] = otp
                st.session_state["username"] = username
                st.session_state["authenticated"] = False
                st.success("OTP sent to your registered email.")
            else:
                st.error("Failed to send OTP. Please try again.")
        else:
            st.error("Invalid username or password.")

    # OTP input section
    if "otp" in st.session_state:
        entered_otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            if entered_otp == str(st.session_state["otp"]):
                st.session_state["authenticated"] = True
                st.success("Login successful!")
            else:
                st.error("Invalid OTP.")

# Register function with OTP verification
def register():
    """Handles the registration process with OTP verification."""
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")

    if st.button("Register"):
        if users_collection.find_one({"username": username}):
            st.error("Username already exists.")
        else:
            hashed_password = hash_password(password)
            # Store user data in MongoDB
            users_collection.insert_one({"username": username, "password": hashed_password, "email": email})
            otp = send_otp(email)  # Send OTP for email verification
            if otp:
                st.session_state["otp"] = otp
                st.session_state["username"] = username
                st.success("OTP sent to your email. Please verify to complete registration.")
            else:
                st.error("Failed to send OTP. Please try again.")

        # OTP input for registration
        entered_otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            if entered_otp == str(st.session_state["otp"]):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Invalid OTP.")

# Stress Analyzer function to analyze and provide feedback
def stress_analyzer():
    """Analyzes the user's stress level and provides feedback and coping strategies."""
    st.header("Study Anxiety Analyzer")

    # Ask user a series of questions to analyze their anxiety levels
    anxiety_level = st.slider("On a scale of 1-10, how stressed are you about your studies?", 1, 10, 5)
    upcoming_exams = st.radio("Do you have any upcoming exams or projects?", ("Yes", "No"))
    sleep_quality = st.radio("How would you rate your sleep quality lately?", ("Good", "Average", "Poor"))
    time_management = st.radio("How confident are you in managing your study time?", ("Very Confident", "Somewhat Confident", "Not Confident"))

    # Provide feedback and tips based on the responses
    if anxiety_level >= 8:
        st.warning("It seems like you're feeling quite stressed. Here are some strategies:") 
        st.write("- Take regular breaks during study sessions to avoid burnout.")
        st.write("- Practice mindfulness and deep breathing exercises to calm your mind.")
        st.write("- Ensure you're getting enough sleep, especially before exams.")
    elif anxiety_level >= 5:
        st.info("You might be experiencing moderate stress. Here are some tips to manage it:")
        st.write("- Prioritize tasks and break them down into smaller, manageable pieces.")
        st.write("- Try using a study schedule or planner to stay organized.")
        st.write("- Take a few minutes each day to relax and recharge.")
    else:
        st.success("It looks like you're handling stress well. Keep up the good work!")
        st.write("- Continue practicing good study habits and maintaining a balanced lifestyle.")
        st.write("- Don't forget to make time for self-care and relaxation.")

    # Suggest daily tips
    st.subheader("Daily Tip to Manage Study and Exam Stress")
    st.write("- Stay positive and focus on what you can control.")
    st.write("- Remember, you're not alone – talk to someone if you feel overwhelmed.")
    st.write("- Regular exercise can help reduce anxiety and improve focus.")

    # Update achievements after stress analysis completion
    if "completed_stress_analysis" not in st.session_state:
        st.session_state["completed_stress_analysis"] = True
        check_achievements()

# Career Guidance function to provide personalized advice
def career_guidance():
    """Provides personalized career advice, scholarships, internships, and quizzes."""
    st.header("Career Guidance")

    # Ask the user about their interests and skills
    interests = st.text_input("What are your main interests or passions? (e.g., technology, health, design)")
    skills = st.text_input("What skills do you have? (e.g., coding, research, writing)")

    if st.button("Get Career Advice"):
        if interests and skills:
            st.subheader("Personalized Career Advice")
            st.write(f"Based on your interests in {interests} and skills in {skills}, here are some career options:")
            st.write("- Software Developer")
            st.write("- Data Scientist")
            st.write("- Researcher in Healthcare")
            st.write("- Marketing Specialist in Tech Industry")
            st.write("- Product Designer")
            st.write("Explore these fields, and find which aligns with your aspirations!")
        else:
            st.error("Please fill in both interests and skills to get career advice.")

    # Provide information on scholarships, internships, and programs
    st.subheader("Scholarships and Programs for Women in STEM")
    st.write("- **[Google Women in Tech Scholarship](https://developers.google.com/womentechmakers)**: A great opportunity for women pursuing computer science and engineering.")
    st.write("- **[Scholarships for Women in STEM](https://www.indiascienceandtechnology.gov.in/nurturing-minds/scholarships/women)**: Find various scholarships for women in science, technology, engineering, and mathematics fields.")

    # Career quiz section
    st.subheader("Career Quiz")
    quiz_answer = st.radio("What kind of work environment do you prefer?", ("Office-based", "Remote", "Freelance"))
    if st.button("Submit Quiz Answer"):
        st.write(f"Great! You prefer a {quiz_answer} work environment. Based on this, you may enjoy jobs that offer flexibility like freelancing or remote work.")

# Career Chatbot feature
def career_chatbot():
    """Simulates a conversation with the Career Chatbot, offering personalized career advice and resources."""
    st.header("Career Chatbot")

    # Display a welcome message for the chatbot
    st.write("Hello! I'm your Career Chatbot. How can I assist you today?")
    
    # Ask user for interests, skills, and career preferences
    user_input = st.text_input("Tell me about your interests or skills...")

    if user_input:
        st.write("Great! I see you're interested in:", user_input)
        
        # Generate personalized career advice based on the input
        st.subheader("Career Advice")
        if "technology" in user_input.lower():
            st.write("You might want to explore careers in Software Development, Data Science, or AI. Consider learning Python or Machine Learning!")
        elif "health" in user_input.lower():
            st.write("You could look into roles like Healthcare Researcher, Nurse, or Public Health Specialist. Consider studying medical sciences or healthcare administration.")
        else:
            st.write("Based on your interests, you could explore careers in various fields. Let's take a look at some educational resources next.")

        # Recommend educational resources based on input
        st.subheader("Recommended Educational Resources")
        st.write("- **[Coursera](https://www.coursera.org)**: Offers courses in a wide range of fields including technology, health, and more.")
        st.write("- **[Udemy](https://www.udemy.com)**: Find practical courses to improve your skills.")
        st.write("- **[edX](https://www.edx.org)**: Take professional certificate programs in technology, business, and health.")

# Achievements tracking
def check_achievements():
    """Check and update achievements based on user actions."""
    if "achievements" not in st.session_state:
        st.session_state["achievements"] = []

    # Check if it's the user's first login
    if "first_login" not in st.session_state:
        st.session_state["achievements"].append("First login")
        st.session_state["first_login"] = True
        st.success("Achievement Unlocked: First login!")

    # Check if stress analysis is completed
    if "completed_stress_analysis" in st.session_state and "Stress Analysis Completed" not in st.session_state["achievements"]:
        st.session_state["achievements"].append("Stress Analysis Completed")
        st.success("Achievement Unlocked: Completed stress analysis!")

    # Check if goals are shared
    if "goals" in st.session_state and "Goals Shared" not in st.session_state["achievements"]:
        st.session_state["achievements"].append("Goals Shared")
        st.success("Achievement Unlocked: Shared goals!")

# Offering daily challenges
def offer_daily_challenges():
    """Offers daily or weekly challenges to users."""
    today = datetime.date.today()
    challenge_key = f"challenge_{today}"

    if challenge_key not in st.session_state:
        st.session_state[challenge_key] = "Not Completed"

        # Example challenge for the user
        st.subheader("Today's Challenge")
        st.write("Complete the Stress Analyzer to unlock today's challenge reward.")
        if st.button("Complete Challenge"):
            st.session_state[challenge_key] = "Completed"
            st.session_state["achievements"].append("Completed Daily Challenge")
            st.success("Challenge Completed! You earned a badge!")

# Inspirational Stories Section
def inspirational_stories():
    st.header("Inspirational Stories of Successful Women")

    # Predefined list of stories (You can extend this with real data or integrate an API)
    stories = [
        {
            "title": "Marie Curie: The Pioneer of Radioactivity",
            "description": "Marie Curie was the first woman to win a Nobel Prize and remains the only woman to win it in two different fields: Physics and Chemistry.",
            "link": "https://www.nobelprize.org/prizes/physics/1903/marie-curie/biographical/"
        },
        {
            "title": "Kalpana Chawla: A Journey to the Stars",
            "description": "Kalpana Chawla was the first woman of Indian origin to go to space, inspiring countless others to pursue their dreams.",
            "link": "https://www.nasa.gov/wp-content/uploads/2020/09/chawla_kalpana.pdf"
        },
        {
            "title": "Sudha Murthy - Philanthropy and Social Impact:",
            "description": "Sudha Murthy is a renowned author, philanthropist, and social worker who has made significant contributions to education and rural development.",
            "link": "https://en.wikipedia.org/wiki/Sudha_Murty"
        },
    ]

    # Display the stories
    for story in stories:
        st.subheader(story["title"])
        st.write(story["description"])
        st.markdown(f"[Read more]({story['link']})")

        # Option to save the story as a favorite
        if st.button(f"Save '{story['title']}' as Favorite", key=story["title"]):
            if "favorites" not in st.session_state:
                st.session_state["favorites"] = []
            if story not in st.session_state["favorites"]:
                st.session_state["favorites"].append(story)
                st.success(f"Saved '{story['title']}' to favorites!")

    # Display saved favorite stories
    if "favorites" in st.session_state and st.session_state["favorites"]:
        st.subheader("Your Favorite Stories")
        for favorite in st.session_state["favorites"]:
            st.write(f"- [{favorite['title']}]({favorite['link']})")

# Emotional Wellness Corner
def emotional_wellness_corner():
    st.header("Emotional Wellness Corner")

    # Section 1: Mindfulness Exercises and Guided Meditations
    st.subheader("Mindfulness Exercises and Guided Meditations")
    st.write("Explore activities to help you relax and find peace:")

    mindfulness_options = ["Deep Breathing", "Body Scan Meditation", "Gratitude Practice"]
    selected_activity = st.radio("Choose an activity:", mindfulness_options)

    if selected_activity == "Deep Breathing":
        st.write("""
        **Deep Breathing Exercise:**
        1. Sit comfortably and close your eyes.
        2. Inhale deeply through your nose for a count of four.
        3. Hold your breath for a count of four.
        4. Exhale slowly through your mouth for a count of six.
        5. Repeat for 5-10 minutes.
        """)
    elif selected_activity == "Body Scan Meditation":
        st.write("""
        **Body Scan Meditation:**
        1. Lie down or sit in a comfortable position.
        2. Close your eyes and focus on your breath.
        3. Slowly bring your attention to each part of your body, starting from your toes and moving upward.
        4. Notice any tension and release it as you exhale.
        """)
    elif selected_activity == "Gratitude Practice":
        st.write("""
        **Gratitude Practice:**
        1. Take a moment to think of three things you're grateful for today.
        2. Write them down or say them out loud.
        3. Reflect on how they bring positivity to your life.
        """)

    # Section 2: Stress-Relief Tips
    st.subheader("Stress-Relief Tips")
    st.write("- Take short breaks during the day to relax your mind.")
    st.write("- Practice self-compassion and remind yourself that it's okay to take things one step at a time.")
    st.write("- Spend time in nature or do something you enjoy.")

    # Section 3: Journaling Tool
    st.subheader("Journaling Tool")
    st.write("Reflect on your emotions and daily experiences. Journaling can help you process your thoughts and improve emotional well-being.")
    
    journal_entry = st.text_area("Write your journal entry here:")
    if st.button("Save Entry"):
        if "journal_entries" not in st.session_state:
            st.session_state["journal_entries"] = []
        st.session_state["journal_entries"].append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "entry": journal_entry
        })
        st.success("Journal entry saved!")

    # Display past journal entries
    if "journal_entries" in st.session_state and st.session_state["journal_entries"]:
        st.subheader("Your Journal Entries")
        for entry in st.session_state["journal_entries"]:
            st.write(f"**Date:** {entry['date']}")
            st.write(f"**Entry:** {entry['entry']}")
            st.write("---")

# Career Preparation Toolkit
def career_preparation_toolkit():
    st.header("Career Preparation Toolkit")

    # Section 1: Resume Templates
    st.subheader("Resume Templates")
    st.write("Download customizable resume templates to create a professional resume.")
    resume_options = {
        "Basic Template": "https://www.canva.com/templates/EAFKBaPgE5g-blue-light-blue-color-blocks-flight-attendant-cv/",
        "Creative Template": "https://www.freepik.com/free-photos-vectors/creative-cv",
        "Professional Template": "https://www.freepik.com/free-photos-vectors/professional-resume"
    }
    for name, link in resume_options.items():
        st.markdown(f"- [{name}]({link})")

    # Section 2: LinkedIn Optimization Tips
    st.subheader("LinkedIn Optimization Tips")
    st.write("Improve your LinkedIn profile to attract recruiters.")
    st.write("""
    - Use a professional profile photo and headline.
    - Write a compelling summary that highlights your achievements and goals.
    - List relevant skills, projects, and certifications.
    - Connect with professionals in your industry and join groups.
    - Keep your profile updated with recent roles and accomplishments.
    """)
    

    # Section 4: AI-Powered Mock Interview Practice
    st.subheader("Mock Interview Practice")
    st.write("Practice answering common interview questions with our AI-powered mock interview tool.")

    question = st.text_input("Answer this question: 'Tell me about yourself.'")
    if st.button("Submit Answer"):
        # Simulate AI response for feedback
        feedback = "Great start! Try to include your professional achievements, skills, and goals in a concise way."
        st.success("Your answer was submitted!")
        st.write(f"**AI Feedback:** {feedback}")

    # Section 5: Industry-Specific Job Boards and Internships
    st.subheader("Job Boards and Internship Resources")
    st.write("Explore these resources to find industry-specific opportunities:")
    job_resources = {
        "Tech Industry Jobs": "https://www.techjobboard.com",
        "Creative Roles": "https://www.creativejobs.com",
        
    }
    for name, link in job_resources.items():
        st.markdown(f"- [{name}]({link})")

    st.info("Pro Tip: Bookmark these resources for easy access!")

# Fashion and Professional Styling Guide
def fashion_styling_guide():
    st.header("Fashion and Professional Styling Guide")

    # User Preferences
    st.subheader("Personalize Your Style")
    gender = st.selectbox("Select your gender:", ["Female", "Male", "Non-binary", "Prefer not to say"])
    occasion = st.radio("What occasion are you preparing for?", ["Interview", "Daily Wear", "Networking Event", "Academic Presentation"])
    style_preference = st.multiselect("What is your preferred style?", ["Formal", "Casual", "Chic", "Minimalist", "Bold"])
    color_preference = st.color_picker("Pick your favorite color for outfits:", "#000000")

    # Generate AI-Powered Recommendations
    if st.button("Get Styling Tips"):
        if not occasion or not style_preference:
            st.error("Please select an occasion and at least one style preference to proceed.")
        else:
            st.subheader("Your Personalized Styling Recommendations")

            # Outfit Suggestions
            st.write(f"**For a {occasion}:**")
            if gender == "Female":
                st.write("- A tailored blazer paired with a pencil skirt or trousers for a professional yet stylish look.")
                st.write(f"- Incorporate your favorite color, {color_preference}, through accessories like scarves or shoes.")
            elif gender == "Male":
                st.write("- A well-fitted suit or blazer with neutral-tone trousers for a classic professional vibe.")
                st.write(f"- Add a pop of your favorite color, {color_preference}, through ties or pocket squares.")
            else:
                st.write("- Neutral, tailored pieces such as structured blazers and comfortable, professional footwear.")
                st.write(f"- Use your favorite color, {color_preference}, in subtle accents like lapel pins or bags.")

            # Grooming Tips
            st.write("**Grooming Tips:**")
            st.write("- Ensure your hair is neat and styled appropriately for the occasion.")
            st.write("- Keep your nails clean and trimmed.")
            st.write("- Use minimal, natural makeup for a polished appearance.")

            # Makeup Advice
            if gender == "Female":
                st.write("**Makeup Advice:**")
                st.write("- Opt for a natural foundation with soft, neutral tones for eyeshadow.")
                st.write("- Avoid overly bright or dramatic colors unless the occasion allows.")
                st.write("- Use a subtle lip color that complements your outfit.")

    # Styling Articles and Resources
    st.subheader("Explore More Resources")
    st.write("- [**Professional Outfit Ideas**](https://www.youtube.com/watch?v=41doIaUBn5I)")
    st.write("- [**10 Grooming Tips for Professionals**](https://www.instyle.com/office-outfit-ideas-5395473)")
    st.write("- [**Styling Guide for Academic Events**](https://www.nykaa.com/beauty-blog/grooming-tips-for-women/)")

    # Save User Preferences
    st.subheader("Save Your Style Preferences")
    if st.button("Save Preferences"):
        preferences = {
            "gender": gender,
            "occasion": occasion,
            "style_preference": style_preference,
            "color_preference": color_preference
        }
        st.session_state["fashion_preferences"] = preferences
        st.success("Preferences saved successfully!")
        st.write("We'll use these preferences for future recommendations.")

# Safe-Space Reporting and Resources
def safe_space_reporting():
    st.header("Safe-Space Reporting and Resources")

    # Information and Resources
    st.subheader("Resources for Support")
    st.write("- [National Domestic Violence Hotline](https://www.thehotline.org): 1-800-799-7233")
    st.write("- [Crisis Text Line](https://www.crisistextline.org): Text HOME to 741741")
    st.write("- [National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org): 988")
    st.write("- [Equal Employment Opportunity Commission (EEOC)](https://www.eeoc.gov): Report workplace discrimination.")
    st.write("- [RAINN - Rape, Abuse & Incest National Network](https://www.rainn.org): 1-800-656-HOPE")
    st.write("- [Find Legal Aid](https://www.lsc.gov/what-legal-aid): Assistance for legal concerns.")

    st.info("These resources are confidential and available to provide assistance.")

    # Anonymous Incident Reporting
    st.subheader("Report an Incident")
    st.write("If you’re facing harassment, bullying, or discrimination, you can report it here anonymously. "
             "Our team will review your report and provide guidance.")

    # Report Form
    incident_type = st.selectbox(
        "What type of incident are you reporting?",
        ["Harassment", "Bullying", "Discrimination", "Other"]
    )
    incident_description = st.text_area(
        "Describe the incident (optional but helpful):",
        placeholder="Provide as much detail as you feel comfortable sharing."
    )
    contact_option = st.checkbox(
        "I consent to being contacted for follow-up (optional).",
        help="If selected, please provide your contact information below."
    )
    contact_info = ""
    if contact_option:
        contact_info = st.text_input("Your contact information (email or phone):")

    if st.button("Submit Report"):
        if incident_type == "Other" and not incident_description:
            st.error("Please provide a description of the incident.")
        else:
            # Save or handle report submission
            report_data = {
                "type": incident_type,
                "description": incident_description,
                "contact_info": contact_info
            }
            # Placeholder for storing the report (e.g., in a database)
            st.success("Thank you for reporting. Your submission has been received and will be reviewed.")

    # Privacy Information
    st.write("**Privacy Notice:**")
    st.write("- All reports are anonymous unless you choose to provide contact information.")
    st.write("- Your data will be handled confidentially and only used to assist you.")

    # Additional Counseling Support
    st.subheader("Request Counseling Support")
    if st.button("Request Counseling Resources"):
        st.info("Our team will share relevant counseling and support resources shortly. Check your notifications.")
        
# Set Preferences & Goals Feature
def set_preferences_and_goals():
    st.header("Set Preferences & Goals")
    preferences = st.text_input("What are your preferences or goals?")
    if st.button("Save Preferences"):
        st.session_state["preferences"] = preferences
        st.success("Preferences saved successfully!")

def fitness_nutrition_guidance():
    """Provides fitness and nutrition guidance, including workouts and meal ideas."""
    st.header("Fitness and Nutrition Guidance")

    # Workout Tutorials Section
    st.subheader("Home Workout Tutorials")
    st.write("Here are some simple home workout tutorials to stay fit:")

    st.markdown("""
    - **[Full Body Home Workout (10 minutes)](https://www.youtube.com/watch?v=zUG2hqw9kLk)**: A quick workout to target your whole body.
    - **[Core Strengthening Routine](https://www.youtube.com/watch?v=iTM98dTBHAA)**: Focuses on strengthening your core muscles.
    - **[Leg Day at Home](https://www.youtube.com/watch?v=Jg61m0DwURs)**: A great workout for toning your legs and glutes.
    """)
    
    # Meal Planning Tips Section
    st.subheader("Meal Planning Tips")
    st.write("Here are some tips for planning balanced and nutritious meals:")

    st.markdown("""
    - **Include protein-rich foods**: such as eggs, beans, and lean meats to fuel your body.
    - **Add vegetables**: Make sure to include a variety of veggies like spinach, broccoli, and carrots for vitamins and minerals.
    - **Stay hydrated**: Drink plenty of water, and consider infusing it with fruits for added flavor.
    - **Plan your meals**: Try to plan and prep your meals ahead of time to avoid unhealthy eating habits.
    """)

    # Snack Ideas Section
    st.subheader("Snack Ideas for Busy Days")
    st.write("Here are some quick and easy snack ideas for busy study or workdays:")

    st.markdown("""
    - **Greek Yogurt with Nuts**: High in protein and healthy fats.
    - **Apple with Peanut Butter**: A balanced snack with fiber, healthy fats, and protein.
    - **Trail Mix**: A mix of nuts, seeds, and dried fruits for a quick energy boost.
    - **Veggie Sticks with Hummus**: Carrot and cucumber sticks with a side of hummus for a healthy, crunchy snack.
    """)

# Main Function
def main():
    st.title("Empower Her App")

    # Sidebar Navigation
    page = st.sidebar.radio("Navigation", ["Login", "Register"])

    if page == "Login":
        login()
    elif page == "Register":
        register()

    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        # Check achievements and offer daily challenges
        check_achievements()
        offer_daily_challenges()

        page = st.sidebar.radio("Navigation", ["Stress Analyzer","Career Guidance", "Career Chatbot","Inspirational Stories","Emotional Wellness Corner","Career Preparation Toolkit","Fashion and Professional Styling Guide","Fitness and Nutrition Guidance"])

        if page == "Stress Analyzer":
            stress_analyzer()
        elif page == "Career Guidance":
            career_guidance()
        
        elif page == "Career Chatbot":
            career_chatbot()
        elif page == "Inspirational Stories":
           inspirational_stories()  
        elif page == "Emotional Wellness Corner":
             emotional_wellness_corner()
        elif page == "Career Preparation Toolkit":
            career_preparation_toolkit()
        elif page == "Fashion and Professional Styling Guide":
            fashion_styling_guide()
        elif page == "Safe-Space Reporting and Resources":
            safe_space_reporting()
        elif page == "Fitness and Nutrition Guidance":
             fitness_nutrition_guidance()
        
# Run the Streamlit app
if __name__ == "__main__":
    main()
