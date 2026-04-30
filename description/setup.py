from glob import glob
from setuptools import setup

package_name = "description"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/urdf", glob("urdf/*.xacro")),
        (f"share/{package_name}/rviz", glob("rviz/*.rviz")),
        (f"share/{package_name}/meshes", glob("meshes/*")),
        (f"share/{package_name}/config", glob("config/*.yaml")),
        (
            f"share/{package_name}/media/materials/scripts",
            glob("media/materials/scripts/*"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@example.com",
    description="URDF/XACRO robot model and posture controller config.",
    license="Apache-2.0",
)
