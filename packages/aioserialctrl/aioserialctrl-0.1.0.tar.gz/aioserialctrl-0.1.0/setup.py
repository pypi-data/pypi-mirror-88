import re
import setuptools
# python setup.py build_ext --inplace

def read_version():
    with open("aioserialctrl/__init__.py") as f:
        return re.search(
            r"""__version__\s+=\s+(['"])(?P<v>.+?)\1""",
            f.read()
        ).group('v')


seriallib_module = setuptools.Extension(
    "seriallib",
    sources=["aioserialctrl/seriallib.c"],
    extra_compile_args=["-lsetupapi"],
    libraries=["setupapi", "Advapi32"],
    language="c",
)

setuptools.setup(
    name="aioserialctrl",
    version=read_version(),
    license="MIT",
    author="eplut",
    author_email="eplutus@protonmail.com",
    description="A module of asyncio serail port control.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eplut/aioserialctrl",
    packages=["aioserialctrl", "aioserialctrl.utils"],
    python_requires=">=3.7",
    platforms="Windows",
    ext_modules=[seriallib_module],
    keywords="serial serialctrl aioserialctrl",
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.7",
    ],
)