import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pomodoro-DEN_ik",
    version="0.0.2",
    author="Denys Zaluzhnyi",
    author_email="denys.zaluzhnyi@gmail.com",
    description="Simple concentrator based on pomodoro technique",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DarkDream99/WorkConcentrator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Home Automation",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        'py-notifier',
    ],
    entry_points="""
        [console_scripts]
        concentrator=work_concentrator.work_concentrator:run
    """,
)
