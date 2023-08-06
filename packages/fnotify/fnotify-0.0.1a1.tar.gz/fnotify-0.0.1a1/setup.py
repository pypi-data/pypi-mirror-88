import setuptools

setuptools.setup(
    name="fnotify",  # Replace with your own username
    version="0.0.1a1",
    author="Fangnikoue Evarist",
    author_email="malevae@gmail.com",
    description="A python program to watch directory and execute any action on contain of directory changed",
    url="https://github.com/eirtscience/inotify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/fnotify'],

    python_requires='>=3.5',
)
