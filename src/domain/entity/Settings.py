class Settings:
    default_type_mapping = {
        "docs": [
            "pdf", "pdf_lbk", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
            "txt", "odt", "ods", "odp"
        ],
        "pics": [
            "jpg", "jpg_lbk", "jpeg", "jpeg_lbk", "png", "gif", "webp"
        ],
        "compressed": [
            "zip", "rar", "tar", "gz", "7z", "xz", "bz2"
        ],
        "audio": [
            "mp3", "wma", "wav", "flac", "ogg", "m4a", "m4a_lbk", "aac"
        ],
        "video": [
            "m4v", "webm", "mp4", "avi", "mkv", "flv", "mov", "wmv"
        ],
        "software": [
            "deb", "exe", "dmg", "pkg", "iso", "img", "apk", "rpm", "pat"
        ],
        "configuration": [
            "json", "so", "ovpn"
        ],
    }

    default_user_settings = {
        "color1": "#0C1821",
        "color2": "#1B2A41",
        "color3": "#324A5F",
        "color4": "#CCC9DC",
        "folder_to_process": "/path/to/folder/to/sort",
        "destination_folder": "/path/to/destination/folder",
        "remove_duplicates_folder": "/path/to/destination/folder",
        "binary_search": True,
        "binary_search_large_files": False,
        "keep_original_files": True,
        "log_output_in_file": True,
        "ask_before_removing_duplicates": True,
        "ask_before_removing_empty_folders": True,
        "binary_comparison_large_files_threshold": 5000000,
    }
