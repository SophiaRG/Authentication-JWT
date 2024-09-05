from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('66b509e618b54a97aeb59acf75b3008d')
    return serializer.dumps(email, salt='SECURITY_PASSWORD_SALT')

def confirm_token(token, salted_password, expiration=3600):
    serializer = URLSafeTimedSerializer('66b509e618b54a97aeb59acf75b3008d')
    try:
        email = serializer.loads(
            token, 
            salt=salted_password,
            max_age=expiration
        )
    except:
        return False
    
    return email