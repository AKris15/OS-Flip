PACKAGE_NAME = os_flip
PYTHON = python3
DIST_DIR = dist

VERSION = $(shell grep -Po "(?<=version=')[^']+" setup.py)

all: clean build upload

clean:
	@echo "🧹 Cleaning previous builds..."
	@rm -rf build/ dist/ *.egg-info

build:
	@echo "📦 Building $(PACKAGE_NAME) version $(VERSION)..."
	@$(PYTHON) setup.py sdist bdist_wheel

upload:
	@echo "🚀 Uploading $(PACKAGE_NAME) to PyPI..."
	@$(PYTHON) -m twine upload $(DIST_DIR)/*

version:
	@echo "🔖 Version: $(VERSION)"

.PHONY: all clean build upload version
