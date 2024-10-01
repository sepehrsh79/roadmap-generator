from src.core.database import DBManager
from src.models import Roadmap
from src.repository.playwright import interact_with_chatgpt
from src.schema.input import InputIn


def complete_prompt(input):
    sample = f"""
    Hello, I want you to help me as someone who knows all the programming stuff

    give me a complete personalized training program based on what I give you as the input parameters

    Input parameter structure (example):
    {{
      "domain": "",
      "level": "",
      "age": 1,
      "goal": "string",
      "learning_style": [],
      "cost_type": "",
      "need_certificate": ,
      "learning_language": "",
      "join_community": ,
      "time_commitment": "",
      "deadline": ""
    }}

    Explanation of the parameters:
    domain: The subject of the educational program (backend development, frontend development, machine learning,  android development or other fields)
    level: (scientific level and my knowledge of the educational topic like No coding experience or Some experience but limited knowledge)
    age: (different people choose different approaches to learning according to their age. Based on my age, suggest the best one)
    goal: (to enter the market, for personal development or to complete a project)
    learning_style: (Video tutorials, Articles and documentation, Interactive coding exercises,Community learning (forums, group projects), etc.):
    cost_type: (does it cost me to access the educational source or not? free or paid)
    learning_language: Trainings should be in the desired language
    need_certificate: (Do I want a training certificate after completing the course?)
    join_community: (if I need, suggest groups and forums related to the educational topic, Telegram, Discord, Reddit, and Instagram)
    time_commitment: (the hours I spend on learn per week)
    deadline: (For example, I have to learn Django in the next 2 months)

    Here is my data parameters:
    {{
      "domain": "{input.domain.value}",
      "level": "{input.level.value}",
      "age": {input.age},
      "goal": "{input.goal}",
      "learning_style": {input.learning_style},
      "cost_type": "{input.cost_type.value}",
      "need_certificate": {input.need_certificate},
      "learning_language": "{input.learning_language}",
      "join_community": {input.join_community},
      "time_commitment": "{input.time_commitment.value}",
      "deadline": "{input.deadline}"
    }}

    Please send me a detailed JSON format of a complete personalized educational program, outlining the step-by-step daily plan until the end of the specified time.
    it should be a daily program
    educational resources and courses, various learning methods, online groups and forums, time planning, course content, course level,course Teacher, course type, course schedule, certificate and fee

    Output data structure :
    {{
      "domain_title": "",
      "description": ""
      "plans": {{
          "day 1": {{
            "educational_resources_link": "",
            "various_learning_methods": "",
            "online_groups_and_forums": "",
            "time_planning": "",
            "course_level": "",
            "course_teacher": "",
            "course_type": "",
            "course": "",
            "has_certificate": "",
            "fee": ""
          }},
          "day 2": ""
            "educational_resources_link": "",
            "various_learning_methods": "",
            "online_groups_and_forums": "",
            "time_planning": "",
            "course_level": "",
            "course_teacher": "",
            "course_type": "",
            "course": "",
            "has_certificate": "",
            "fee": ""
          }},
      }}
    }}
    """
    return sample


# def process_gpt_responses_to_dict(
#     first_resp, second_resp) -> Tuple[str, str]:
#     body = first_resp["text"]
#     second_resp_tags = None
#     try:
#         second_resp_text = re.search(
#             r'\{.*\}', second_resp["text"].replace("'", "\"")
#         )
#         if not second_resp_text:
#             raise exceptions.NoJsonFound(
#                 "No valid JSON object found in the last line"
#             )
#         second_resp_text = second_resp_text.group()
#         second_resp_tags: list = json.loads(second_resp_text)["keywords"]
#         if "#YES" in first_resp["text"].upper():
#             second_resp_tags.append("yes")
#         elif "#NO" in first_resp["text"].upper():
#             second_resp_tags.append("no")
#         else:
#             second_resp_tags.append("na")
#         second_resp_tags.extend([job_mode, country])
#         hashtags = ' '.join(set(f"#{tag}" for tag in second_resp_tags))
#         body = f"""{first_resp["text"]}
#             {hashtags}
#         """
#     except (json.JSONDecodeError, KeyError, ValueError) as error:
#         loguru.logger.error(
#             f"Error happened parsing responses from thebai: {error}"
#         )
#     finally:
#         return (body, second_resp_tags)



async def create_roadmap_in_background(input: InputIn, db_session: DBManager):
    result = complete_prompt(input)
    response = await interact_with_chatgpt(result)
    # response_dict = process_gpt_responses_to_dict(response)
    roadmap = Roadmap(**response)
    db_session.add(roadmap)
    db_session.commit()
    db_session.refresh(roadmap)

