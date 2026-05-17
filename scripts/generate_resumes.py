"""
Generate optimized synthetic resumes for the AI Hiring Agent.

Goals:
- strong semantic retrieval
- meaningful ranking differentiation
- explainability support
- refinement support
- comparison support
- multi-round screening realism

Run:
    python scripts/generate_resumes.py

Optional:
    python scripts/generate_resumes.py --clean
"""

from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESUME_DIR = BASE_DIR / "data" / "resumes"


ROLE_SKILLS = {
    "React Developer": [
        "React",
        "TypeScript",
        "Redux",
        "Next.js",
        "HTML",
        "CSS",
        "JavaScript",
        "REST APIs",
        "Jest",
        "Webpack",
    ],
    "Flask Backend Engineer": [
        "Python",
        "Flask",
        "SQLAlchemy",
        "PostgreSQL",
        "Redis",
        "Celery",
        "Docker",
        "JWT",
        "REST APIs",
        "Microservices",
    ],
    "MERN Stack Developer": [
        "MongoDB",
        "Express.js",
        "React",
        "Node.js",
        "Redux",
        "TypeScript",
        "JWT",
        "REST APIs",
        "Docker",
        "AWS",
    ],
    "Java Spring Boot Engineer": [
        "Java",
        "Spring Boot",
        "Hibernate",
        "Kafka",
        "Redis",
        "MySQL",
        "Microservices",
        "Docker",
        "JUnit",
        "AWS",
    ],
    "ML Engineer": [
        "Python",
        "PyTorch",
        "TensorFlow",
        "Pandas",
        "NumPy",
        "LangChain",
        "RAG",
        "Vector Databases",
        "AWS",
        "Docker",
    ],
    "DevOps Engineer": [
        "AWS",
        "Docker",
        "Kubernetes",
        "Terraform",
        "CI/CD",
        "Linux",
        "Prometheus",
        "Grafana",
        "Ansible",
        "Monitoring",
    ],
}


FIRST_NAMES = [
    "John",
    "Alice",
    "David",
    "Sophia",
    "Michael",
    "Emma",
    "Daniel",
    "Olivia",
    "James",
    "Charlotte",
    "Ethan",
    "Mia",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Brown",
    "Williams",
    "Miller",
    "Davis",
    "Wilson",
    "Taylor",
    "Anderson",
    "Thomas",
]


COMPANIES = [
    "TechNova",
    "CloudScale",
    "InnovateX",
    "DataForge",
    "NextWave",
    "ByteWorks",
    "HyperSoft",
    "CodeSphere",
]


ACHIEVEMENTS = [
    "Reduced API latency by 40%",
    "Improved deployment speed by 60%",
    "Led migration to microservices architecture",
    "Built scalable cloud-native systems on AWS",
    "Optimized PostgreSQL queries for high traffic workloads",
    "Improved frontend performance and Lighthouse scores",
    "Automated CI/CD pipelines reducing manual effort",
    "Implemented monitoring and alerting systems",
]


GENERIC_SKILLS = [
    "AWS",
    "Docker",
    "Redis",
    "Kafka",
    "CI/CD",
    "GraphQL",
    "Kubernetes",
    "Agile",
    "Microservices",
]


QUALITY_TYPES = [
    "strong",
    "good",
    "borderline",
    "weak",
]


def ensure_directory():
    RESUME_DIR.mkdir(parents=True, exist_ok=True)


def clean_existing():
    if RESUME_DIR.exists():
        shutil.rmtree(RESUME_DIR)


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_summary(role: str, quality: str):
    summaries = {
        "strong": (
            f"Experienced {role} with strong expertise in scalable systems, "
            f"cloud-native architecture, CI/CD, and production-grade engineering."
        ),
        "good": (
            f"{role} with practical experience building modern applications "
            f"and collaborating in agile engineering teams."
        ),
        "borderline": (
            f"{role} with moderate experience and growing exposure "
            f"to scalable backend/frontend systems."
        ),
        "weak": (
            f"Early-career {role} with foundational development experience "
            f"and eagerness to learn modern engineering practices."
        ),
    }

    return summaries[quality]


def generate_projects(quality: str):
    project_count = {
        "strong": 4,
        "good": 3,
        "borderline": 2,
        "weak": 1,
    }[quality]

    return random.sample(ACHIEVEMENTS, project_count)


def build_skill_profile(role_skills: list[str], quality: str):
    if quality == "strong":
        selected = random.sample(role_skills, min(8, len(role_skills)))
        selected += random.sample(GENERIC_SKILLS, 4)

    elif quality == "good":
        selected = random.sample(role_skills, min(6, len(role_skills)))
        selected += random.sample(GENERIC_SKILLS, 3)

    elif quality == "borderline":
        selected = random.sample(role_skills, min(4, len(role_skills)))
        selected += random.sample(GENERIC_SKILLS, 2)

    else:
        selected = random.sample(role_skills, min(3, len(role_skills)))
        selected += random.sample(GENERIC_SKILLS, 1)

    return list(set(selected))


def generate_resume(role: str, skills: list[str], idx: int):
    name = random_name()

    quality = random.choice(QUALITY_TYPES)

    if quality == "strong":
        experience = random.randint(5, 8)

    elif quality == "good":
        experience = random.randint(3, 5)

    elif quality == "borderline":
        experience = random.randint(2, 4)

    else:
        experience = random.randint(1, 2)

    final_skills = build_skill_profile(skills, quality)

    projects = generate_projects(quality)

    company = random.choice(COMPANIES)

    leadership = quality in ["strong", "good"]

    leadership_text = (
        "Led engineering initiatives and mentored junior developers."
        if leadership
        else "Collaborated with senior engineers in agile teams."
    )

    achievements_text = "\n".join(f"- {p}" for p in projects)

    summary = generate_summary(role, quality)

    certification = random.choice(
        [
            "AWS Certified Developer",
            "Docker Certified Associate",
            "Azure Fundamentals",
            "Google Cloud Associate",
            "None",
        ]
    )

    startup_experience = random.choice([True, False])

    startup_text = (
        "Worked in fast-paced startup environments with rapid product iterations."
        if startup_experience
        else "Worked in structured enterprise engineering teams."
    )

    resume_text = f"""
{name}

Role:
{role}

Experience:
{experience} years

Current Company:
{company}

Skills:
{", ".join(final_skills)}

Professional Summary:
{summary}

Key Achievements:
{achievements_text}

Leadership:
{leadership_text}

Work Style:
{startup_text}

Certifications:
{certification}

Additional Keywords:
scalable systems, REST APIs, agile development, production deployment,
system design, debugging, performance optimization, cloud infrastructure
"""

    filename = (
        RESUME_DIR /
        f"{role.lower().replace(' ', '_')}_{idx}.txt"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(resume_text.strip())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing generated resumes first",
    )

    args = parser.parse_args()

    if args.clean:
        clean_existing()

    ensure_directory()

    print("=" * 80)
    print("Generating optimized synthetic resumes")
    print("=" * 80)

    total_resumes = 0

    for role, skills in ROLE_SKILLS.items():

        for idx in range(1, 8):
            generate_resume(role, skills, idx)
            total_resumes += 1

    print(f"Generated resumes: {total_resumes}")
    print(f"Saved to: {RESUME_DIR}")

    print("\nDone.")


if __name__ == "__main__":
    main()