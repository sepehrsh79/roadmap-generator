import enum


class LevelEnum(enum.Enum):
    absolute_beginner = "No coding experience"
    beginner = "Some experience but limited knowledge"
    intermediate = "Comfortable with basic coding concepts"
    advanced = "Looking to specialize"


class LearningStyleEnum(enum.Enum):
    video_tutorials = "Video tutorials"
    articles_and_documentation = "Articles and documentation"
    interactive_exercises = "Interactive coding exercises"
    community_learning = "Community learning (forums, group projects)"


class CostTypeEnum(enum.Enum):
    free = "Free"
    paid = "Paid"
    both = "Free and Paid"


class TimeCommitmentEnum(enum.Enum):
    less_than_5 = "Less than 5 hours per week"
    _5_10 = "5 to 10 hours per week"
    _10_20 = "10 to 20 hours per week"
    more_than_20 = "More than 20 hours per week"


class DomainEnum(enum.Enum):
    backend_development = "Back-End Development"
    frontend_development = "Front-End Development"
    data_science = "Data Science"
    machine_learning = "Machine Learning"
    artificial_intelligence = "Artificial Intelligence"
    ui_ux = "UI/UX"
    ios_development = "IOS Development"
    android_development = "Android Development"
    hardware_programming = "Hardware Programming"
    blockchain = "Blockchain"
    game_development = "game Development"
    dev_ops = "DevOps"
    cybersecurity_development = "CyberSecurity Development"
