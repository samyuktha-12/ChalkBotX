from setuptools import setup, find_packages

# Read the project description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ChalkBotX",
    version="1.0.0",
    author="Samyuktha",
    description="An Interactive Chatbot to help with Academic Queries",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt')
    ],
    python_requires=">=3.11",
)
