import io
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()

about = {}
with io.open(
    os.path.join(here, "grvlmsfigures", "__about__.py"), "rt", encoding="utf-8"
) as f:
    exec(f.read(), about)


setup(
    name="grvlms-figures",
    version=about["__version__"],
    url="https://groove.education/",
    project_urls={
        "Documentation": "https://groove.education/",
        "Code": "https://github.com/groovetch/grvlms-figures",
        "Issue tracker": "https://github.com/groovetch/grvlms-figures/issues",
        "Community": "https://groove.education/",
    },
    license="AGPLv3",
    author="Overhang.io",
    author_email="thuan.ha@grovoetechnology.com",
    description="A Grvlms plugin for Figures, the Open edX reporting and data retrieval app",
    long_description=readme,
    long_description_content_type='text/x-rst',
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=["grvlms-openedx<10.0.0"],
    python_requires=">=3.5",
    entry_points={"grvlms.plugin.v0": ["figures = grvlmsfigures.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
