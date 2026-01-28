for dir in */; do
    if [ -d "$dir" ]; then
        touch "$dir/__init__.py"
    else
        echo "$dir is not a directory."
    fi
done
	
