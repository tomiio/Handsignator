import pyttsx3

def typing(text):
    mapping = {
        'aa': 'â',
        'aw': 'ă',
        'af': 'à',
        'as': 'á',
        'ar': 'ả',
        'ax': 'ã',
        'aj': 'ạ',
        'awf': 'ằ',
        'aws': 'ắ',
        'awr': 'ẳ',
        'awx': 'ẵ',
        'awj': 'ặ',
        'aaf': 'ầ',
        'aas': 'ấ',
        'aar': 'ẩ',
        'aax': 'ẫ',
        'aaj': 'ậ',
        'ef': 'è',
        'es': 'é',
        'er': 'ẻ',
        'ex': 'ẽ',
        'ej': 'ẹ',
        'ee': 'ê',
        'eef': 'ề',
        'ees': 'ế',
        'eer': 'ể',
        'eex': 'ễ',
        'eej': 'ệ',
        'if': 'ì',
        'is': 'í',
        'ir': 'ỉ',
        'ix': 'ĩ',
        'ij': 'ị',
        'ow': 'ơ',
        'oo': 'ô',
        'of': 'ò',
        'os': 'ó',
        'or': 'ỏ',
        'ox': 'õ',
        'oj': 'ọ',
        'oof': 'ồ',
        'oos': 'ố',
        'oor': 'ổ',
        'oox': 'ỗ',
        'ooj': 'ộ',
        'owf': 'ờ',
        'ows': 'ớ',
        'owr': 'ở',
        'owx': 'ỡ',
        'owj': 'ợ',
        'uw': 'ư',
        'uf': 'ù',
        'us': 'ú',
        'ur': 'ủ',
        'ux': 'ũ',
        'uj': 'ụ',
        'uuf': 'ừ',
        'uus': 'ứ',
        'uur': 'ử',
        'uux': 'ữ',
        'uwj': 'ự',
        'yf': 'ỳ',
        'ys': 'ý',
        'yr': 'ỷ',
        'yx': 'ỹ',
        'yj': 'ỵ',
        'dd': 'đ',
    }
    


    text1 = text.replace("_", " ")

    typing_text = text1 + '...'
    st1 = ""
    st2 = ""

    for i in range(len(typing_text)-2):

        st1 = typing_text[i] + typing_text[i+1]
        st2 = typing_text[i] + typing_text[i+1] + typing_text[i+2]
        if st2 in mapping:
            text1 = text1.replace(st2, mapping[st2])
            pass
        elif st1 in mapping:
            text1 = text1.replace(st1, mapping[st1])
            pass

    return text1

# Fix text
text = input("Nhập văn bản tiếng Việt: ")
text_fix = typing(text)
print("Văn bản sau khi biến đổi:",text_fix)

engine = pyttsx3.init()
engine.setProperty('voice', 'vi')  # Replace <voice_id> with the ID of the Vietnamese voice you want to use

rate = engine.getProperty('rate')   # Get the current speech rate
engine.setProperty('rate', rate-35) # Decrease the rate by 50 (adjust as needed)

engine.say(text_fix)
engine.runAndWait()
