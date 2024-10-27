import random

def generate_otp() -> str:
    otp = ""
    otp_length = 6
    for i in range(otp_length): 
        otp += str(random.randint(0, 9))
    return otp