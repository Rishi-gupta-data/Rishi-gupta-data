import requests
from bs4 import BeautifulSoup
import re

# Replace with your actual W3Schools public profile URL
W3SCHOOLS_PROFILE_URL = "https://www.w3schools.com/users/profile.asp?username=Rishi-Gupta"

def fetch_w3schools_progress():
    response = requests.get(W3SCHOOLS_PROFILE_URL)
    if response.status_code != 200:
        print("Failed to fetch W3Schools profile")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    skills = {}

    for skill in soup.find_all("div", class_="skill-bar"):  # Update class based on W3Schools HTML
        skill_name = skill.find("span", class_="skill-name").text.strip()
        progress_text = skill.find("div", class_="progress-bar").get("style")  # Example: "width: 80%;"
        progress = re.search(r"(\d+)%", progress_text)

        if progress:
            skills[skill_name] = progress.group(1)

    return skills

def update_readme(skills):
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()

    start_marker = "<!-- W3SCHOOLS_SKILLS_START -->"
    end_marker = "<!-- W3SCHOOLS_SKILLS_END -->"

    new_skills_content = start_marker + "\n"
    for skill, level in skills.items():
        new_skills_content += f"**{skill}**  \n![{skill}](https://progress-bar.dev/{level}/?title={skill.replace(' ', '%20')})\n"
    new_skills_content += end_marker

    updated_content = re.sub(f"{start_marker}.*?{end_marker}", new_skills_content, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("README.md updated successfully!")

if __name__ == "__main__":
    skills = fetch_w3schools_progress()
    if skills:
        update_readme(skills)
