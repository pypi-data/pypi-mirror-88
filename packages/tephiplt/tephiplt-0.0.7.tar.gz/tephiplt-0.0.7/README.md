Welcome to my repository for education and outreach code.  Below are details about code for tephigram plotting and global warming experiments

# Tephigram Plotting
The tephi_plt code allows users to plot the following isopleths as presented in tephigrams: temperature, potential temperature, wet bulb potential temperature, pressure and water mixing ratio.  To ensure dependecies are installed, the pip setup is recommended:

i) at the command line create a virtual environment in a suitable location (the environment will also contain the tephigram plotting package) using at least python 3: python3 -m venv tephi_env

ii) activate this virtual environment: source tephi_env/bin/activate

iii) ensure pip up to date in this environment: pip install --upgrade pip

iv) move to where tephigram plotting package to be installed: cd tephi_env/lib/python3.7/site_packages

v) install the package: python -m pip install --upgrade tephiplt

You are now ready to run the package:

i) when sure of being inside the site_packages directory of the virtual environment run code: python tephiplt