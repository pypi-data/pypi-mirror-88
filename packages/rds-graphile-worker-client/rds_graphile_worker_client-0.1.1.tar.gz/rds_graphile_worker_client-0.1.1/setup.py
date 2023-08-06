from setuptools import find_packages, setup

version_info = {}
exec(open("rds_graphile_worker_client/package_version.py").read(), version_info)

# readme = open("README.md", "rb").read().decode("utf-8")
install_requires = open("requirements.txt", "rb").read().decode("utf-8")

setup(
    name="rds_graphile_worker_client",
    version=version_info["__version__"],
    description="A small, simple client for adding jobs to the graphile-worker job queue on RDS postgresql database",
    # long_description=readme,
    # long_description_content_type="text/markdown",
    author="Curvewise",
    author_email="jacob@curvewise.com",
    url="https://github.com/curvewise/python-rds-graphile-worker-client",
    project_urls={
        "Issue Tracker": "https://github.com/curvewise/python-rds-graphile-worker-client/issues"
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
