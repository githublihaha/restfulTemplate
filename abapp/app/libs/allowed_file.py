def allowed_file(filename, allowed):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()