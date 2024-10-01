import json
from uuid import UUID

from src.core.database import DBManager
from src.crud.roadmap import RoadmapCRUD
from src.repository.playwright import interact_with_chatgpt
from src.schema.input import InputIn


def complete_prompt(input):
    sample = f"""
    Hello, I want you to help me as someone who knows all the programming stuff

    give me a complete personalized training program based on what I give you as the input parameters

    Input parameter structure (example):
    {{
      "domain": "",
      "specific_tool": "",
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
    specific_tool: the tool or technology like a framework or library that i want to learn. this specific tools should be part of our domain (Example django, react, HTML, express, ...)
                    you should create training program with domain field when we dont have specific_tool but if we have specific_tool, you SHOULD create training program with specific_tool
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
      "specific_tool": "{input.specific_tool}",
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


async def process_gpt_responses(resp: str, user_id:UUID, db_session: DBManager) -> tuple:
    try:
        start_index = resp.find('{')
        end_index = resp.rfind('}') + 1
        json_string = resp[start_index:end_index]
        data = json.loads(json_string)

        roadmap_data = {"topic": data.get("domain_title"),
                        "description":data.get("description")
                        }
        roadmap = await RoadmapCRUD.create_roadmap(db_session=db_session, user_id=user_id, **roadmap_data)

        learning_days = []
        for index, day in data.get("plans").items():
            day_data = {"title":index,
                        "course_link":day.get("educational_resources_link"),
                        "learning_methods":day.get("various_learning_methods"),
                        "online_groups_and_forums":day.get("online_groups_and_forums"),
                        "course":day.get("course"),
                        "course_level":day.get("course_level"),
                        "course_teacher":day.get("course_teacher"),
                        "course_type":day.get("course_type"),
                        "time_planning":day.get("time_planning"),
                        "fee":day.get("fee"),
                        "has_certificate":day.get("has_certificate"),
                        }
            day = await RoadmapCRUD.create_learning_day(db_session, roadmap_id=roadmap.id, **day_data)
            learning_days.append(day)
        return roadmap, learning_days
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        raise Exception(str(error))


async def create_roadmap_in_background(input: InputIn, user_id:UUID, db_session: DBManager):
    result = complete_prompt(input)
    response = None
    for i in range(3):
        response = await interact_with_chatgpt(result)
        if response:
            break
    await process_gpt_responses(resp=response, user_id=user_id, db_session=db_session)
