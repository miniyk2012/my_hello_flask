SECRET_KEY = "12345"
WTF_CSRF_ENABLED = True
WTF_I18N_ENABLED = False
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 最大文件上传大小限制
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

# Flask-CKEditor config
# CKEDITOR_SERVE_LOCAL = True
# CKEDITOR_FILE_UPLOADER = 'upload_for_ckeditor'

# Flask-Dropzone config
DROPZONE_ALLOWED_FILE_CUSTOM = True
DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt'
DROPZONE_MAX_FILE_SIZE = 30  # 最大30M
DROPZONE_MAX_FILES = 1000
DROPZONE_REDIRECT_VIEW = "show_images"

