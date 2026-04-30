from setuptools import setup

package_name = "control"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@example.com",
    description="Motion manager for the loaf cat robot.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "motion_manager = control.motion_manager:main",
        ],
    },
)
