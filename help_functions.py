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

def bayes_conversion(users_a, users_b, conv_a, conv_b, n_samples=100_000):
    """
    Сравнивает вторую когорту с первой по бета-распределению конверсий:
    - расчитывается вероятность того, что конверсия второй выше, чем у первой;
    - ожидаемые потери, если выбрать "неправильную" группу.
    """
    alpha_a, beta_a = conv_a + 1, users_a + 1 - conv_a 
    alpha_b, beta_b = conv_b + 1, users_b + 1 - conv_b
    samples_a = np.random.beta(alpha_a, beta_a, size=n_samples)
    samples_b = np.random.beta(alpha_b, beta_b, size=n_samples)
    probability_b_better = np.mean(samples_b > samples_a)

    loss_if_A = np.mean(np.maximum(samples_b - samples_a, 0))
    loss_if_B = np.mean(np.maximum(samples_a - samples_b, 0))

    return {
            'prob': round(probability_b_better * 100, 2),
            'loss_if_A': round(loss_if_A * 100, 2),
            'loss_if_B': round(loss_if_B * 100, 2),
            }

def welch_test_two_groups(group_a_data, group_b_data, min_cnt=1000):
    """
    Сравнение двух групп по среднему значению метрики при помощи t-теста Уэлча. 
    Уэлч подходит для сравнения средних значений даже при неравных дисперсиях и размерах выборок.
    Хорошо работает на больших выборках (> 1000 наблюдений на группу) благодаря цпт даже при ненормальных распределениях.
    """
    cnt_a, mean_a, std_a, mean_real_a  = group_a_data['cnt'], group_a_data['mean'], group_a_data['std'], group_a_data['mean_real']
    cnt_b, mean_b, std_b, mean_real_b  = group_b_data['cnt'], group_b_data['mean'], group_b_data['std'], group_b_data['mean_real']

    if cnt_a < min_cnt or cnt_b < min_cnt:
        return {
                'p-value': None,
                'is_significant': False,
                'Стат.значимость': 'Мало данных для корректного подсчёта'
                }

    se_a = std_a**2 / cnt_a
    se_b = std_b**2 / cnt_b
    t_stat = (mean_b - mean_a) / np.sqrt(se_a + se_b)
    df = (se_a + se_b)**2 / ((se_a**2)/(cnt_a - 1) + (se_b**2)/(cnt_b - 1))
    
    p_value = 2 * t.sf(np.abs(t_stat), df)
    is_significant = p_value < 0.05
    mean_diff_real = mean_real_b - mean_real_a
    mean_diff_log = mean_b - mean_a
    sign_raw = np.sign(mean_diff_real)
    sign_log = np.sign(mean_diff_log)
    
    if is_significant and sign_raw != sign_log:
        reason = 'Неопределённость, возможно киты/выбросы'
    elif is_significant:
        reason = '2 значимо лучше 1' if mean_diff_real > 0 else '2 значимо хуже 1'
    else:
        reason = 'Нет значимости'
    
    return {
            'p-value': round(p_value, 5),
            'is_significant': is_significant,
            'Стат.значимость': reason
            }
