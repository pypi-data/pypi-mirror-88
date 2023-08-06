from setuptools import setup


setup(name='yahtzee_api',
      version='0.2.0',
      description='A general purpose API to play an n-player game of Yahtzee programmatically. Useful for algorithm development, intended for future use with custom OpenAI Gym Yahtzee RL environments.',
      long_description='Welcome to the Yahtzee API! This package provides the core functionalities to programmatically play a game of Yahtzee. The stated purpose of this package is for use with custom OpenAI Gym reinforcement learning environments (in development), however it is generalized for many different use cases, including simple algorithm development. As this is the first full iteration of this API, I will likely be reworking/adding to some of the core functionalities to suit my needs once I do more work on the OpenAI Gym environments that will be using this package.',
      url='https://github.com/tomarbeiter/yahtzee_api',
      author='Tom Arbeiter',
      license='Apache 2.0',
      packages=['yahtzee_api'],
      install_requires=['pytest', 'sphinx'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        'Intended Audience :: Developers',
    ],
)