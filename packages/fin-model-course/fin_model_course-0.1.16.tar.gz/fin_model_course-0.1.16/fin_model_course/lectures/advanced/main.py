from courses.config import COURSES
from courses.model import CourseSelectors
from lectures.advanced import notes
from lectures.model import LectureGroup
from resources.models import RESOURCES
from schedule.main import LECTURE_13_NAME


def get_advanced_modeling_lecture() -> LectureGroup:
    lecture_index = 1
    title = LECTURE_13_NAME
    course = COURSES[CourseSelectors.ADVANCED]
    description = "Gives a quick overview of more advanced material that we didn't have time to cover. " \
                  "Includes resources to go out an learn the advanced material, so this lecture can be " \
                  "viewed as a road-map for future learning. This is also a jumping off point for the " \
                  "Advanced Financial Modeling with Python course"
    resources = [
        *RESOURCES.lectures.advanced.resources(),
    ]
    lectures = [
        notes.get_intro_advanced_lecture(),
        notes.get_model_types_lecture(),
        notes.get_data_pipelines_lecture(),
        notes.get_math_tools_lecture(),
        notes.get_present_model_lecture(),
        notes.get_programming_lecture(),
        notes.get_extras_lecture(),
    ]
    return LectureGroup(title, description, lectures, order=lecture_index, global_resources=resources, course=course)
