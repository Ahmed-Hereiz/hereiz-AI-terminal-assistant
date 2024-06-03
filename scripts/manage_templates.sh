input_text=""

cd src/managment/manage_templates/ || { echo "Error: Directory 'src/managment/manage_templates/' not found."; exit 1; }

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -t)
            shift
            input_text="$1"
            bash ./template_t.sh "$1"
            ;;
        -tl)
            bash ./template_tl.sh
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done