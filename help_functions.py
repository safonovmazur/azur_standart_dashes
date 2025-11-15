# ВСПОМОГАТЕЛЬНЫЕ ФУНЦИИ
def days_to_str(days):
    """
    Функция выбора слова 'дней'/'дня'.
    """  
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    elif days % 10 in [2, 3, 4] and not (days % 100 in [12, 13, 14]):
        return f"{days} дня"
    else:
        return f"{days} дней"

def print_html(text, msg_type="info"):
    """
    Печатает html-сообщение заданным стилем.
    """
    styles = {
            "error": "#ff0065",
            "info": "#7393B3",
            }
    color = styles.get(msg_type, "#000000")
    print(f"%html <h6><span style='color:{color}; font-size:13px'>{text}<br></span></h6>")
