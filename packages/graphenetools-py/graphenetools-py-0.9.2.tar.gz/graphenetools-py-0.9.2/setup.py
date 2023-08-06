import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="graphenetools-py",
    version="0.9.2",
    description="Tools for generating parameters for helium on uniaxially strained graphene simulations using quantum Monte Carlo software hosted at https://code.delmaestro.org and plots of the helium graphene interaction",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nscottnichols/graphenetools-py",
    author="Nathan Nichols",
    author_email="Nathan.Nichols@uvm.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["graphenetools"],
    include_package_data=True,
    install_requires=["numpy", "matplotlib", "scipy"],
    entry_points={
        "console_scripts": [
            "gt_roughly_square=graphenetools.gt_roughly_square:main",
            "gt_rs=graphenetools.gt_roughly_square:main",
            "gt_c_one_third_commensurate_command=graphenetools.gt_c_one_third_commensurate_command:main",
            "gt_cotcc=graphenetools.gt_c_one_third_commensurate_command:main",
            "gt_roughly_square_plot=graphenetools.gt_roughly_square_plot:main",
            "gt_rsp=graphenetools.gt_roughly_square_plot:main",
            "gt_c_one_third_commensurate_command_plot=graphenetools.gt_c_one_third_commensurate_command_plot:main",
            "gt_cotccp=graphenetools.gt_c_one_third_commensurate_command_plot:main",
        ]
    },
)
