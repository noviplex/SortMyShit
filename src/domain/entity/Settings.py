class Settings:
    defaultTypeMapping = {
        "docs": ["pdf", "pdf_lbk", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "odt", "ods", "odp"],
        "pics": ["jpg", "jpg_lbk", "jpeg", "jpeg_lbk", "png", "gif", "webp"],
        "compressed": ["zip", "rar", "tar", "gz", "7z", "xz", "bz2"],
        "audio": ["mp3", "wma", "wav", "flac", "ogg", "m4a", "m4a_lbk", "aac"],
        "video": ["m4v", "webm", "mp4", "avi", "mkv", "flv", "mov", "wmv"],
        "software": ["deb", "exe", "dmg", "pkg", "iso", "img", "apk", "rpm", "pat"],
        "configuration": ["json", "so", "ovpn"],
    }
    defaultUserSettings = {
        "fontColor": "#BDB6D0",
        "backgroundColor": "#46464C",
        "folderToProcess": "/path/to/folder/to/sort",
        "destinationFolder": "/path/to/destination/folder",
        "removeDuplicatesFolder": "/path/to/destination/folder",
        "binarySearch": True,
        "binarySearchLargeFiles": False,
        "keepOriginalFiles": True,
        "logOutputInFile": True,
        "askBeforeRemovingDuplicates": True,
        "askBeforeRemovingEmptyFolders": True,
        "binaryComparisonLargeFilesThreshold": 5000000,
    }
