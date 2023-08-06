import setuptools

with open("README.md", "r") as f:
    descriptions = f.read()

setuptools.setup(
    name="billing_audit", # Replace with your own username
    version="0.0.4",
    author="vuonglv",
    author_email="vuonglv@vccloud.vn",
    description="Billing audit utils",
    long_description=descriptions,
    long_description_content_type="text/markdown",
    url="https://git.paas.vn/devteam/billing/audit-services/audit-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
