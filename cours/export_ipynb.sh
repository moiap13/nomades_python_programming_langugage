#!/bin/bash

ENV_NAME="nomades_notebook_convert"
INPUT_PATH="./jupyter"
OUTPUT_PATH="./pdfs"
FORMAT_OPTIONS=("HTML" "PDF" "WebPDF" "Markdown" "Python" "Slides" "LaTeX")
FORMAT_EXTENSIONS=("html" "pdf" "webpdf" "md" "py" "slides" "tex")
DEFAULT_FORMAT_INDEX=2

check_and_create_env() {
    if conda env list | grep -q "^${ENV_NAME} "; then
        echo "Environment '${ENV_NAME}' already exists."
    else
        echo "Environment '${ENV_NAME}' does not exist. Creating..."
        conda create -y -n "${ENV_NAME}" python=3.11
    fi
}

check_and_install_packages() {
    local packages=("nbconvert" "pandoc" "jupyter")
    local missing_packages=()

    for package in "${packages[@]}"; do
        if ! conda run -n "${ENV_NAME}" conda list "${package}" 2>/dev/null | grep -q "${package}"; then
            missing_packages+=("${package}")
        fi
    done

    if [ ${#missing_packages[@]} -gt 0 ]; then
        echo "Installing missing packages: ${missing_packages[*]}"
        conda install -y -n "${ENV_NAME}" "${missing_packages[@]}"
    else
        echo "All required packages are installed."
    fi

    echo "Installing weasyprint and system dependencies..."
    conda install -y -n "${ENV_NAME}" -c conda-forge weasyprint cairo pango gdk-pixbuf pycairo 2>/dev/null || \
    conda install -y -n "${ENV_NAME}" -c conda-forge weasyprint 2>/dev/null || \
    conda run -n "${ENV_NAME}" pip install weasyprint
}

read -p "Enter the path for ipynb notebook files [${INPUT_PATH}]: " user_input_path
if [ -n "${user_input_path}" ]; then
    INPUT_PATH="${user_input_path}"
fi

read -p "Enter the output path for converted files [${OUTPUT_PATH}]: " user_output_path
if [ -n "${user_output_path}" ]; then
    OUTPUT_PATH="${user_output_path}"
fi

echo "Select output format:"
for i in "${!FORMAT_OPTIONS[@]}"; do
    echo "  $((i+1)) - ${FORMAT_OPTIONS[$i]}"
done

read -p "Enter format number [3 (${FORMAT_OPTIONS[$DEFAULT_FORMAT_INDEX]})]: " format_choice
if [ -z "${format_choice}" ]; then
    format_choice=$((DEFAULT_FORMAT_INDEX + 1))
fi

format_index=$((format_choice - 1))
if [ "${format_index}" -lt 0 ] || [ "${format_index}" -gt 6 ]; then
    echo "Invalid format choice. Defaulting to WebPDF."
    format_index=${DEFAULT_FORMAT_INDEX}
fi

OUTPUT_FORMAT="${FORMAT_OPTIONS[$format_index]}"
if [ "${OUTPUT_FORMAT}" == "WebPDF" ]; then
    OUTPUT_EXT="pdf"
else
    OUTPUT_EXT="${FORMAT_EXTENSIONS[$format_index]}"
fi

echo ""
echo "Configuration:"
echo "  Input path: ${INPUT_PATH}"
echo "  Output path: ${OUTPUT_PATH}"
echo "  Format: ${OUTPUT_FORMAT}"
echo ""

check_and_create_env
check_and_install_packages

EXECUTE_FLAG=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --execute)
            EXECUTE_FLAG="--execute"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

mkdir -p "${OUTPUT_PATH}"

if [ -f "${INPUT_PATH}" ] && [[ "${INPUT_PATH}" == *.ipynb ]]; then
    ipynb_files=("${INPUT_PATH}")
elif [ -d "${INPUT_PATH}" ]; then
    shopt -s nullglob
    ipynb_files=("${INPUT_PATH}"/*.ipynb)
else
    echo "Invalid input: ${INPUT_PATH} is neither a .ipynb file nor a directory"
    exit 1
fi

if [ ${#ipynb_files[@]} -eq 0 ]; then
    echo "No .ipynb files found in ${INPUT_PATH}"
    exit 0
fi

echo "Converting ${#ipynb_files[@]} notebook(s)..."

failed_conversions=()
successful_conversions=()

for notebook in "${ipynb_files[@]}"; do
    filename=$(basename "${notebook}" .ipynb)
    output_file="${OUTPUT_PATH}/${filename}.${OUTPUT_EXT}"

    echo "Converting: ${notebook} -> ${output_file}"

    if [ "${OUTPUT_FORMAT}" == "PDF" ] || [ "${OUTPUT_FORMAT}" == "WebPDF" ]; then
        temp_html="${OUTPUT_PATH}/temp_${filename}.html"
        if conda run -n "${ENV_NAME}" jupyter nbconvert --to html "${EXECUTE_FLAG}" "${notebook}" --output-dir "${OUTPUT_PATH}" --output "temp_${filename}.html" 2>/dev/null; then
            if conda run -n "${ENV_NAME}" python -c "
import sys
try:
    from weasyprint import HTML
    HTML('${temp_html}').write_pdf('${output_file}')
    import os
    os.remove('${temp_html}')
    sys.exit(0)
except Exception as e:
    print(f'weasyprint failed: {e}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null; then
                successful_conversions+=("${filename}")
                echo "  Success!"
            else
                echo "  HTML->PDF via weasyprint failed, trying pandoc..."
                rm -f "${temp_html}"
                failed_conversions+=("${filename}")
                echo "  FAILED"
            fi
        else
            failed_conversions+=("${filename}")
            echo "  FAILED - HTML conversion failed"
        fi
    else
        if conda run -n "${ENV_NAME}" jupyter nbconvert --to "${OUTPUT_FORMAT}" "${EXECUTE_FLAG}" "${notebook}" --output-dir "${OUTPUT_PATH}" --output "${filename}.${OUTPUT_EXT}" 2>&1; then
            successful_conversions+=("${filename}")
            echo "  Success!"
        else
            failed_conversions+=("${filename}")
            echo "  FAILED"
        fi
    fi
    echo ""
done

echo "=========================================="
echo "Conversion complete!"
echo "Successful: ${#successful_conversions[@]}"
echo "Failed: ${#failed_conversions[@]}"

if [ ${#failed_conversions[@]} -gt 0 ]; then
    echo ""
    echo "Failed notebooks:"
    for f in "${failed_conversions[@]}"; do
        echo "  - ${f}"
    done
fi