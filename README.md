# Threat Detection Score

A Python package for cybersecurity threat analysis and detection. This package provides tools to assess detection coverage, organizational alignment, and threat severity using LangChain and OpenAI integrations.

## Features

- **Detection Coverage Analysis**: Evaluate detection capabilities using OpenAI and LangChain.
- **Organizational Alignment**: Align cybersecurity practices with organizational goals.
- **Threat Severity Assessment**: Determine the severity of cybersecurity threats.
- **Command-Line Tools**: Console scripts for streamlined operations.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Install the Package

1. Clone the repository:

   ```powershell
   git clone https://github.com/zhazhalove/threat_detection_score_py_package.git
   Set-Location threat_detection_score_py_package
   ```

2. Install the package:

   ```powershell
   pip install .
   ```

3. (Optional) Install in editable mode for development:

   ```powershell
   pip install -e .
   ```

4. Using PowerShell Module - MicromambaTools (https://github.com/zhazhalove/MicromambaTools)
   ```powershell
   Install-PackagesInMicromambaEnvironment -EnvName "langchain" -Packages @("$PWD\threat_detection_score_py_package")
   ```

## Usage

### Command-Line Tools

The package provides the following console scripts:

1. **Detection Coverage**

   ```powershell
   detection_coverage --help
   ```

   Use this tool to evaluate detection coverage.

2. **Organizational Alignment**

   ```powershell
   org_alignment --help
   ```

   Use this tool to align cybersecurity practices with organizational goals.

3. **Threat Severity**
   ```powershell
   threat_severity --help
   ```
   Use this tool to assess the severity of cybersecurity threats.

### Example

```powershell
# Run detection coverage analysis
python -m detection_coverage --human-message-input "some text"

python -m detection_coverage --human-message-input "some text" --temperature "0.0" --model-name "gpt-4o-mini" --max-retries "3"

# Align organizational practices
python -m org_alignment --human-message-input "some text"

python -m org_alignment --human-message-input "some text" --temperature "0.0" --model-name "gpt-4o-mini" --max-retries "3"

# Assess threat severity
python -m threat_severity --human-message-input "some text"

python -m reat_severity --human-message-input "some text" --temperature "0.0" --model-name "gpt-4o-mini" --max-retries "3"

```

## Dependencies

The following packages are required:

- `typer`
- `langchain`
- `langchain-openai`

Dependencies are automatically installed when the package is installed.

## License

This project is licensed under the MIT License. See the [LICENSE].
