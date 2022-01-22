#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-audio-anarchy.jarbasai=skill_audio_anarchy:AudioAnarchySkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-audio-anarchy',
    version='0.0.1',
    description='ovos audio anarchy skill plugin',
    url='https://github.com/JarbasSkills/skill-audio-anarchy',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_audio_anarchy": ""},
    package_data={'skill_audio_anarchy': ['locale/*', 'res/*', 'ui/*']},
    packages=['skill_audio_anarchy'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
