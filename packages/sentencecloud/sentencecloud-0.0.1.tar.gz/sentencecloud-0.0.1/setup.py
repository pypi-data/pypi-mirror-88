import io
from setuptools import setup
from setuptools.extension import Extension
import versioneer

with io.open('README.md', encoding='utf_8') as fp:
    readme = fp.read()

setup(
    author="Rajesh Prabhu",
    author_email="",
    name='sentencecloud',
    version="0.0.1",
    #cmdclass=versioneer.get_cmdclass(),
    url='https://github.com/eRajsh/sentence_cloud',
    description='A little sentence cloud generator',
    long_description=readme,
    long_description_content_type='text/markdown; charset=UTF-8',
    license='MIT',
    install_requires=['numpy>=1.6.1', 'pillow', 'matplotlib'],
    ext_modules=[Extension("sentencecloud.query_integral_image",
                           ["sentencecloud/query_integral_image.c"])],
    entry_points={'console_scripts': ['wordcloud_cli=sentencecloud.__main__:main']},
    packages=['sentencecloud'],
    package_data={'sentencecloud': ['stopwords', 'MuseoModerno-Bold.ttf']}
)
