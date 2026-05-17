"""
Generate optimized synthetic job descriptions for the AI Hiring Agent.

Goals:
- meaningful retrieval
- ranking differentiation
- refinement testing
- explainability testing
- multi-round screening support

Run:
    python scripts/generate_jds.py

Optional:
    python scripts/generate_jds.py --clean
"""

from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
JD_DIR = BASE_DIR / "data" / "jds"


ROLE_CONFIG = {
    "React Developer": {
        "must_have": [
            "React",
            "TypeScript",
            "Redux",
            "REST APIs",
            "JavaScript",
        ],
        "nice_to_have": [
            "AWS",
            "Docker",
            "CI/CD",
            "Next.js",
            "Jest",
        ],
    },
    "Flask Backend Engineer": {
        "must_have": [
            "Python",
            "Flask",
            "PostgreSQL",
            "REST APIs",
            "SQLAlchemy",
        ],
        "nice_to_have": [
            "Docker",
            "Redis",
            "AWS",
            "Celery",
            "Microservices",
        ],
    },
    "MERN Stack Developer": {
        "must_have": [
            "MongoDB",
            "Express.js",
            "React",
            "Node.js",
            "Redux",
        ],
        "nice_to_have": [
            "AWS",
            "Docker",
            "TypeScript",
            "CI/CD",
            "GraphQL",
        ],
    },
    "Java Spring Boot Engineer": {
        "must_have": [
            "Java",
            "Spring Boot",
            "Hibernate",
            "Microservices",
            "MySQL",
        ],
        "nice_to_have": [
            "Kafka",
            "Redis",
            "AWS",
            "Docker",
            "JUnit",
        ],
    },
    "ML Engineer": {
        "must_have": [
            "Python",
            "PyTorch",
            "TensorFlow",
            "LangChain",
            "RAG",
        ],
        "nice_to_have": [
            "AWS",
            "Docker",
            "Vector Databases",
            "CI/CD",
            "MLOps",
        ],
    },
    "DevOps Engineer": {
        "must_have": [
            "AWS",
            "Docker",
            "Kubernetes",
            "Terraform",
            "CI/CD",
        ],
        "nice_to_have": [
            "Prometheus",
            "Grafana",
            "Linux",
            "Monitoring",
            "Ansible",
        ],
    },
}


COMPANIES = [
    "TechNova",
    "CloudScale",
    "InnovateX",
    "DataForge",
    "NextWave",
    "ByteWorks",
]


RESPONSIBILITIES = [
    "Build scalable production-grade systems",
    "Collaborate with cross-functional engineering teams",
    "Participate in architecture and design discussions",
    "Improve system reliability and performance",
    "Write maintainable and testable code",
    "Contribute to CI/CD and deployment workflows",
    "Participate in agile software development processes",
]


BONUS_TRAITS = [
    "startup experience",
    "leadership skills",
    "strong communication",
    "system design exposure",
    "cloud-native development experience",
    "problem-solving ability",
]


def ensure_directory():
    JD_DIR.mkdir(parents=True, exist_ok=True)


def clean_existing():
    if JD_DIR.exists():
        shutil.rmtree(JD_DIR)


def generate_jd(role: str, config: dict, idx: int):
    must_have = random.sample(config["must_have"], 4)

    nice_to_have = random.sample(config["nice_to_have"], 3)

    experience_required = random.randint(2, 6)

    company = random.choice(COMPANIES)

    responsibilities = random.sample(RESPONSIBILITIES, 4)

    bonus_traits = random.sample(BONUS_TRAITS, 2)

    hiring_level = random.choice(
        [
            "Junior",
            "Mid-Level",
            "Senior",
        ]
    )

    if hiring_level == "Senior":
        leadership_line = (
            "Prior experience leading engineering initiatives is preferred."
        )

    else:
        leadership_line = (
            "Ability to collaborate effectively in agile engineering teams."
        )

    jd_text = f"""
Company:
{company}

Job Title:
{hiring_level} {role}

Experience Required:
{experience_required}+ years

Must Have Skills:
- {chr(10).join(must_have)}

Nice To Have Skills:
- {chr(10).join(nice_to_have)}

Responsibilities:
- {chr(10).join(responsibilities)}

Preferred Candidate Traits:
- {chr(10).join(bonus_traits)}

Additional Expectations:
{leadership_line}

Keywords:
scalable systems, REST APIs, agile development,
production deployment, cloud infrastructure,
performance optimization, debugging, CI/CD
"""

    filename = (
        JD_DIR /
        f"jd_{role.lower().replace(' ', '_')}_{idx}.txt"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(jd_text.strip())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing generated JDs first",
    )

    args = parser.parse_args()

    if args.clean:
        clean_existing()

    ensure_directory()

    print("=" * 80)
    print("Generating optimized synthetic job descriptions")
    print("=" * 80)

    total_jds = 0

    for role, config in ROLE_CONFIG.items():

        for idx in range(1, 4):
            generate_jd(role, config, idx)
            total_jds += 1

    print(f"Generated job descriptions: {total_jds}")
    print(f"Saved to: {JD_DIR}")

    print("\nDone.")


if __name__ == "__main__":
    main()