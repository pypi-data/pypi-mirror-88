from setuptools import setup
from setuptools.extension import Extension

setup(
    author="Rajesh Prabhu",
    author_email="",
    name='sentence_cloud',
    version="0.0.0.2",
    description="A small sentence cloud generator package",
    long_description="A small sentence cloud generator package, based on amueller's word cloud package",
    long_description_content_type="text/markdown",
    url="https://github.com/eRajsh/sentence_cloud",
    license='MIT',
    install_requires=['numpy>=1.6.1', 'pillow', 'matplotlib'],
    ext_modules = [Extension("sentencecloud.query_integral_image",
                             ["sentencecloud/query_integral_image.c"])],
    entry_points={'console_scripts': ['wordcloud_cli=wordcloud.__main__:main']},
    packages=['sentencecloud'],
    package_data={'sentencecloud': ['stopwords', 'MuseoModerno-Bold.ttf']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)

